import json
import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

start = time.time()

BASE_URL = "http://quotes.toscrape.com/js/"
url = BASE_URL

quotes = []

res = requests.get(url)
soup = BeautifulSoup(res.content, "lxml")

scripts = soup.find_all("script")

for s in scripts:
    if s.string and "var data =" in s.string:
        script = s.string
        break

# Extract JSON data from the JavaScript variable
# (\[.*?\]) matches the JSON array
match = re.search(r"var data = (\[.*?\]);", script, re.DOTALL)
data = json.loads(match.group(1))

for q in data:
    quote = q["text"].strip('“”')
    author = q["author"]["name"]
    tags = q["tags"]
    quotes.append({
        "text": quote,
        "author": author,
        "tags": ", ".join(tags),
    })

# Save to CSV
df = pd.DataFrame(quotes)
df.to_csv("data/quotesJs.csv", index=False)

# Print time taken
end = time.time()
print(f"Scraping completed in {end - start:.2f} seconds.")