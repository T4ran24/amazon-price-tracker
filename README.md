This Python script tracks an Amazon product by requesting its product detail page and extracting the product title and price from the returned HTML. It uses a persistent requests Session with realistic browser headers and first loads the Amazon homepage to obtain cookies, which helps reduce bot detection and inconsistent page responses.

After requesting the product page, the script parses the HTML using BeautifulSoup and searches for the product title and price using multiple fallback selectors. This is necessary because Amazon frequently changes its page structure, and the title or price can appear in different elements depending on layout, discounts, or A/B testing. If the standard product title selector is missing, the script also checks alternative title locations and Open Graph metadata.

The script includes basic detection logic to determine whether the received page is a real product page or a variant such as a delivery-location gate, cookie consent page, or bot-protection response. If the first attempt returns a valid HTTP status but does not contain the expected data, the script automatically retries once using the same session and cookies.

Finally, the program prints the extracted product name, price, HTTP status code, and diagnostic hints when data cannot be found. This approach makes the scraper more stable against Amazon’s dynamic layouts while remaining suitable for educational and testing purposes.

<img width="1686" height="294" alt="image" src="https://github.com/user-attachments/assets/a6b496d3-4682-495c-b5a8-22835b574e8d" />
