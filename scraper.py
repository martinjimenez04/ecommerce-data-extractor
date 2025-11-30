import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL without page number placeholder
base_url = "http://books.toscrape.com/catalogue/page-{}.html"

books_data = []
page_number = 1

# User-Agent to mimic a real browser request
headers = {
    "User-Agent": "Mozilla/5.0"
}

print("Starting bulk scraping...")

while True:
    # Construct current page URL
    url = base_url.format(page_number)
    
    response = requests.get(url, headers=headers)
    
    # If page returns 404 (Not Found), we reached the end
    if response.status_code != 200:
        print(f"End of catalogue reached at page {page_number}. Finishing...")
        break

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    
    # Safety check: if page exists but has no books
    if not books:
        break

    print(f"Scraping page {page_number}...")

    for book in books:
        # Extract title
        title = book.h3.find("a")["title"]
        
        # Extract and clean price
        raw_price = book.find("p", class_="price_color").text
        price = raw_price.replace("Â£", "£")
        
        # Extract availability status
        availability = book.find("p", class_="instock availability").text.strip()

        books_data.append({
            "Title": title,
            "Price": price,
            "Availability": availability
        })
    
    # Move to next page
    page_number += 1
    
    # IMPORTANT: Delay to prevent server overload (Anti-bot best practice)
    time.sleep(1)

# Save data to CSV with English filename
output_file = "full_catalogue.csv"
df = pd.DataFrame(books_data)
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"Success! {len(books_data)} books saved to '{output_file}'.")