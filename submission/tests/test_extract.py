from unittest import TestCase, mock
import datetime
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError, RequestException
import unittest

import utils.extract as ext

# ─── DUMMY RESPONSES FOR mocking requests.Session ───────────────────────────────
class DummyResponse:
    def __init__(self, status_code=200, content=b"", exc=None):
        self.status_code = status_code
        self.content = content
        self._exc = exc

    def raise_for_status(self):
        if self._exc:
            raise self._exc


class DummySession:
    def __init__(self, responses):
        # responses: list of DummyResponse instances or Exceptions
        self._iter = iter(responses)

    def get(self, url, headers, timeout):
        resp = next(self._iter)
        if isinstance(resp, Exception):
            raise resp
        return resp


class TestFetchingContent(TestCase):
    def setUp(self):
        # bypass delay
        patcher = mock.patch('utils.extract.time.sleep', return_value=None)
        self.addCleanup(patcher.stop)
        patcher.start()

    def test_200_ok(self):
        session = DummySession([DummyResponse(200, b"OK")])
        with mock.patch('utils.extract.requests.Session', return_value=session):
            result = ext.fetching_content('http://example.com', retries=1, timeout=1, backoff=0)
            self.assertEqual(result, b"OK")

    def test_404_returns_none(self):
        session = DummySession([DummyResponse(404, b"")])
        with mock.patch('utils.extract.requests.Session', return_value=session):
            result = ext.fetching_content('http://example.com', retries=1, timeout=1, backoff=0)
            self.assertIsNone(result)

    def test_http_error_then_success(self):
        session = DummySession([
            DummyResponse(500, b"", HTTPError("500 Error")),
            DummyResponse(200, b"YAY")
        ])
        with mock.patch('utils.extract.requests.Session', return_value=session):
            result = ext.fetching_content('url', retries=2, timeout=1, backoff=0)
            self.assertEqual(result, b"YAY")

    def test_all_requests_fail(self):
        # simulate RequestException on all retries
        exceptions = [RequestException("fail")] * 3
        session = DummySession(exceptions)
        with mock.patch('utils.extract.requests.Session', return_value=session):
            result = ext.fetching_content('url', retries=3, timeout=1, backoff=0)
            self.assertIsNone(result)


class TestExtractData(TestCase):
    def test_extract_data_complete(self):
        # wrap product-details inside collection-card
        html = """
        <div class="product-details">
          <h3 class="product-title">My Shirt</h3>
          <div class="price-container">
            <span class="price">$123</span>
          </div>
          <p style="font-size: 14px; color: #777;">4.8 stars</p>
          <p style="font-size: 14px; color: #777;">Blue, Black</p>
          <p style="font-size: 14px; color: #777;">L</p>
          <p style="font-size: 14px; color: #777;">Men</p>
        </div>
        """
        wrapper = f"<div class='collection-card'>{html}</div>"
        tag = BeautifulSoup(wrapper, 'html.parser').div
        out = ext.extract_data(tag)

        self.assertEqual(out['Title'], 'My Shirt')
        self.assertEqual(out['Price'], '$123')
        self.assertEqual(out['Rating'], '4.8 stars')
        self.assertEqual(out['Colors'], 'Blue, Black')
        self.assertEqual(out['Size'], 'L')
        self.assertEqual(out['Gender'], 'Men')
        self.assertIsInstance(out['Timestamp'], datetime.datetime)

    def test_extract_data_missing(self):
        # empty product-details inside collection-card triggers exception path
        html = "<div class='product-details'></div>"
        wrapper = f"<div class='collection-card'>{html}</div>"
        tag = BeautifulSoup(wrapper, 'html.parser').div
        out = ext.extract_data(tag)

        # all fields set to 'Not found' on exception
        self.assertEqual(out['Title'], 'Not found')
        self.assertEqual(out['Price'], 'Not found')
        self.assertEqual(out['Rating'], 'Not found')
        self.assertEqual(out['Colors'], 'Not found')
        self.assertEqual(out['Size'], 'Not found')
        self.assertEqual(out['Gender'], 'Not found')


class TestScrapeProduct(TestCase):
    def setUp(self):
        # bypass sleep delays
        patcher = mock.patch('utils.extract.time.sleep', return_value=None)
        self.addCleanup(patcher.stop)
        patcher.start()

    def make_card_html(self, title="T", price="$1", rating="R", colors="C", size="S", gender="G"):
        return f"""
        <div class=\"collection-card\"> 
          <div class=\"product-details\"> 
            <h3 class=\"product-title\">{title}</h3>
            <p class=\"price\">{price}</p>
            <p style=\"font-size: 14px; color: #777;\">{rating}</p>
            <p style=\"font-size: 14px; color: #777;\">{colors}</p>
            <p style=\"font-size: 14px; color: #777;\">{size}</p>
            <p style=\"font-size: 14px; color: #777;\">{gender}</p>
          </div>
        </div>
        """

    def make_page(self, cards_html, next_disabled=False, next_exists=True):
        next_li = ''
        if next_disabled:
            next_li = "<li class='next disabled'>Next</li>"
        elif next_exists:
            next_li = "<li class='next'>Next</li>"
        return f"<html><body>{cards_html}{next_li}</body></html>"

    def test_pagination(self):
        pages = [
            self.make_page(self.make_card_html('A', '$10', '5 stars', 'Red', 'M', 'Unisex'), next_exists=True),
            self.make_page(self.make_card_html('B', '$20', '4 stars', 'Blue', 'L', 'Women'), next_disabled=True),
            None
        ]
        with mock.patch('utils.extract.fetching_content', side_effect=pages):
            data = ext.scrape_product('http://fake/')
            self.assertEqual(len(data), 2)
            self.assertEqual([d['Title'] for d in data], ['A','B'])

    def test_no_cards(self):
        html = self.make_page('', next_exists=False)
        with mock.patch('utils.extract.fetching_content', return_value=html):
            data = ext.scrape_product('http://fake/')
            self.assertEqual(data, [])


if __name__ == '__main__':
    unittest.main()