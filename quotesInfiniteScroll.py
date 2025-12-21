import time

import pandas as pd
import requests

start = time.time()

session = requests.Session()
page = 1
quotes = []

while True:
    url = f"http://quotes.toscrape.com/api/quotes?page={page}"
    res = session.get(url)
    data = res.json()   # Get JSON response
    
    for q in data["quotes"]:
        quote = q["text"].strip('“”')
        author = q["author"]["name"]
        tags = q["tags"]
        quotes.append({
            "text": quote,
            "author": author,
            "tags": ", ".join(tags),
        })
    
    if not data["has_next"]:
        break
    
    page += 1

df = pd.DataFrame(quotes)
df.to_csv("data/quotesScroll.csv", index=False)

end = time.time()
print(f"Scraping completed in {end - start:.2f} seconds.")