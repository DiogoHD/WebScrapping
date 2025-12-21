import time
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

start = time.time()

login_url = "http://quotes.toscrape.com/login"
session = requests.Session()

# Login to the site
res = session.get(login_url)
soup = BeautifulSoup(res.content, "lxml")
csrf_token = soup.find("input", {"name": "csrf_token"})["value"]
payload = {
    "csrf_token": csrf_token,
    "username": "user",
    "password": "pass"
}
login_res = session.post(login_url, data=payload)

if login_res.status_code == 200:
    print("Login successful")
else:
    print("Login failed")

# Now scrape the quotes pages
url = "http://quotes.toscrape.com/"
quotes = []
while url:
    res = session.get(url)
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
    
    # Handle pagination
    next_button = soup.find("li", class_="next")
    next_link = next_button.find("a")["href"] if next_button else None
    url = urljoin(url, next_link) if next_link else None

# Save to CSV
df = pd.DataFrame(quotes)
df.to_csv("data/quotesLogin.csv", index=False)

# Print time taken
end = time.time()
print(f"Scraping completed in {end - start:.2f} seconds.")