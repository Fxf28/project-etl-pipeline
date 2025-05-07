import time
import logging
import datetime
import requests
from bs4 import BeautifulSoup

# ─── CONFIG LOGGING ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ─── USER-AGENT ─────────────────────────────────────────────────────────────────
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

# ─── FETCHING CONTENT ────────────────────────────────────────────────────────────
def fetching_content(url, retries=3, timeout=10, backoff=2):
    """GET HTML dengan retry, timeout, dan logging. 404 dianggap 'halaman selesai'."""
    session = requests.Session()

    for attempt in range(1, retries + 1):
        try:
            logging.info(f"Requesting {url} (attempt {attempt}/{retries})")
            resp = session.get(url, headers=HEADERS, timeout=timeout)
            # cek status
            if resp.status_code == 404:
                logging.info(f"404 Not Found → anggap akhir pagination: {url}")
                return None
            resp.raise_for_status()
            return resp.content

        except requests.exceptions.HTTPError as e:
            # selain 404, HTTPError lain
            logging.warning(f"HTTP error for {url} (attempt {attempt}): {e}")
        except requests.exceptions.RequestException as e:
            # timeout, DNS failure, dll
            logging.warning(f"RequestException for {url} (attempt {attempt}): {e}")

        # kalau masih ada retries
        if attempt < retries:
            time.sleep(backoff)
        else:
            logging.error(f"All {retries} attempts failed for {url}. Skipping.")
            return None

    # Hanya untuk kepuasan linting, seharusnya tak terpanggil
    return None

# ─── EXTRACT DATA ───────────────────────────────────────────────────────────────
def extract_data(collection):
    """Parse satu product card → dict dengan try-except dan timestamp."""
    try:
        prod = collection.find('div', class_='product-details') or BeautifulSoup('', 'html.parser')

        # Title
        h3 = prod.find('h3', class_='product-title')
        title = h3.text.strip() if h3 else "Title not found"

        # Price
        price = ''
        pc = prod.find('div', class_='price-container')
        if not pc:
            price = prod.find('p', class_='price').text.strip()
        else:
            span_price = pc.find('span', class_='price')
            if span_price:
                price = span_price.text.strip()

        # Paragraphs (rating, colors, size, gender)
        ps = prod.find_all('p', style='font-size: 14px; color: #777;')
        rating = ps[0].text.strip() if len(ps) > 0 else "Rating not found"
        colors = ps[1].text.strip() if len(ps) > 1 else "Colors not found"
        size   = ps[2].text.strip() if len(ps) > 2 else "Size not found"
        gender = ps[3].text.strip() if len(ps) > 3 else "Gender not found"

    except Exception as e:
        logging.error(f"Error extracting product data: {e}")
        title = price = rating = colors = size = gender = "Not found"

    # timestamp
    ts = datetime.datetime.now()
    return {
        "Title": title,
        "Price": price,
        "Rating": rating,
        "Colors": colors,
        "Size": size,
        "Gender": gender,
        "Timestamp": ts
    }

# ─── SCRAPE PRODUCT ────────────────────────────────────────────────────────────
def scrape_product(base_url, start_page=1, delay=1):
    """Loop through pages, collect all product dicts hingga halaman 404."""
    data = []
    page = start_page

    while True:
        url = base_url if page == 1 else f"{base_url}page{page}"
        logging.info(f"Scraping page {page}: {url}")

        html = fetching_content(url)
        if html is None:
            # Jika None karena 404 atau kegagalan total → selesai
            logging.info("Reached end of pagination — scraping complete.")
            break

        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.find_all('div', class_='collection-card')
        if not cards:
            logging.warning(f"No products found on page {page}. Assuming end.")
            break

        for card in cards:
            try:
                data.append(extract_data(card))
            except Exception as e:
                logging.error(f"Failed to parse one collection-card: {e}")

        # Cek tombol next yang disabled secara eksplisit
        next_li = soup.find('li', class_='next')
        if next_li and 'disabled' in next_li.get('class', []):
            logging.info("Next button disabled — scraping complete.")
            break
        elif next_li:
            page += 1
            time.sleep(delay)
        else:
            logging.info("No next-button found — scraping complete.")
            break

    return data