from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

BASE_URL = "https://books.toscrape.com/"
url = BASE_URL
RATING_DICT = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
progress_bar = tqdm(desc="Scraping books", unit="page")

books = []
with requests.Session() as session:
    while url:
        res = session.get(url)
        soup = BeautifulSoup(res.content, "html.parser")
        books_soup = soup.find_all("article", class_="product_pod")

        for b in books_soup:
            title = b.find("h3").find("a")["title"]
            price = b.find("p", class_="price_color").text
            rating = b.find("p", class_="star-rating")["class"][1]
            in_stock = b.find("p", class_="instock availability").text.strip().lower()
            
            book = {
            "title": title,
            "price": price,
            "rating": RATING_DICT[rating],
            "in_stock": True if "in stock" in in_stock else False,
            }
            books.append(book)
        
        next_button = soup.find("li", class_="next")
        next_link = next_button.find("a")["href"] if next_button else None
        url = urljoin(url, next_link) if next_link else None
        
        progress_bar.update(1)

df = pd.DataFrame(books)
df.to_csv("data/books.csv", index=False)

progress_bar.close()