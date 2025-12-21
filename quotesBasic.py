import time
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

start = time.time()

BASE_URL = "http://quotes.toscrape.com/"
url = BASE_URL

quotes = []
while url:
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "lxml")

    quotes_soup = soup.find_all("div", class_="quote")

    for q in quotes_soup:
        quote = q.find("span", class_="text").text.strip('“”')
        author = q.find("small", class_="author").text
        tags = [tag.text for tag in q.find_all("a", class_="tag")]
        quotes.append({
            "text": quote,
            "author": author,
            "tags": ", ".join(tags),
        })
    
    next_button = soup.find("li", class_="next")
    next_link = next_button.find("a")["href"] if next_button else None
    url = urljoin(url, next_link) if next_link else None

df = pd.DataFrame(quotes)
df.to_csv("data/quotesBasic.csv", index=False)

end = time.time()
print(f"Scraping completed in {end - start:.2f} seconds.")