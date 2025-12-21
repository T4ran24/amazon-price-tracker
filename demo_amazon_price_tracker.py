import requests
from bs4 import BeautifulSoup

PRODUCT_URL = "https://www.amazon.com/dp/B0D8JWD2WF"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

def clean_text(tag):
    return tag.get_text(strip=True) if tag else None

try:
    r = requests.get(PRODUCT_URL, headers=headers, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    title_tag = soup.select_one("#productTitle") or soup.select_one("h1#title")
    title = clean_text(title_tag)

    price_tag = (
        soup.select_one("span.a-offscreen") or
        soup.select_one("#priceblock_ourprice") or
        soup.select_one("#priceblock_dealprice") or
        soup.select_one("span.a-price-whole")
    )
    price = clean_text(price_tag)

    if title:
        print("Product:", title)
    else:
        print("Title not found – Amazon may block your request.")

    if price:
        print("Price:", price)
    else:
        print("Price not found – Amazon may hide price or block request.")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
