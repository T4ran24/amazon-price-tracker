import requests
from bs4 import BeautifulSoup

PRODUCT_URL = "https://www.amazon.com/dp/B0D8JWD2WF"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
}

def clean(tag):
    return tag.get_text(" ", strip=True) if tag else None

def extract_title(soup):
   
    return (
        clean(soup.select_one("#productTitle")) or
        clean(soup.select_one("h1#title span")) or
        clean(soup.select_one("h1.a-size-large span")) or
        clean(soup.select_one("meta[property='og:title']")) 
    )

def extract_price(soup):
    
    candidates = [
        "span.a-offscreen",
        "#corePriceDisplay_desktop_feature_div span.a-offscreen",
        "#corePrice_feature_div span.a-offscreen",
        "#priceblock_ourprice",
        "#priceblock_dealprice",
        "#price_inside_buybox",
        "span.a-price-whole",
    ]
    for sel in candidates:
        tag = soup.select_one(sel)
        if tag:
            txt = clean(tag)
           
            if txt and any(ch.isdigit() for ch in txt):
                return txt
    return None

def looks_like_product_page(html: str) -> bool:
    h = html.lower()
   
    return ("producttitle" in h) or ("add-to-cart" in h) or ("buybox" in h) or ("/dp/" in h)

def debug_hint(r_text: str):
    low = r_text.lower()
    if "captcha" in low or "robot check" in low:
        return "bot-check/captcha page"
    if "choose your location" in low or "deliver to" in low:
        return "delivery/location gate page"
    if "consent" in low and "cookies" in low:
        return "cookie consent page"
    return "unknown variant page"

session = requests.Session()
session.headers.update(HEADERS)

try:
   
    session.get("https://www.amazon.com/", timeout=15)

 
    for attempt in [1, 2]:
        r = session.get(PRODUCT_URL, timeout=15)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        title = clean(soup.select_one("#productTitle")) or clean(soup.select_one("h1#title span"))
        price = extract_price(soup)

       
        if not title:
            og = soup.select_one("meta[property='og:title']")
            if og and og.get("content"):
                title = og.get("content").strip()

        if title or price:
            print("Product:", title if title else "Title not found")
            print("Price:", price if price else "Price not found")
            print("Status:", r.status_code)
            break

        if attempt == 1:
            print("Attempt 1: got Status 200 but no title/price.")
            print("Hint:", debug_hint(r.text))
            print("Page length:", len(r.text))

            session.get(PRODUCT_URL + "?th=1&psc=1", timeout=15)

    else:
        print("Still no title/price after retry.")
        print("Status:", r.status_code)
        print("Hint:", debug_hint(r.text))
        print("Final URL:", r.url)
        print("Page length:", len(r.text))

except requests.exceptions.RequestException as e:
    print("Request failed:", e)
