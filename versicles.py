import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import time

start = time.time()

BASE_URL = "https://www.bibliaon.com/versiculos_biblicos/"
url = BASE_URL
session = requests.Session()

versicles = []
while url:
    res = session.get(url)
    print(url)
    soup = BeautifulSoup(res.content, "lxml")
    
    versicles_soup = soup.find_all("div", class_="destaque versiculo-card")
    for v in versicles_soup:
        p_tag = v.find("p")
        a_tag = p_tag.find("a")

        versicle = a_tag.text.strip() if a_tag else ""
        
        if a_tag:
            a_tag.decompose()  # Removes and deletes <a>
        
        content = p_tag.text.strip() if p_tag else ""
        
        versicles.append({
            "versicle": versicle,
            "content": content,
        })
    
    next_button = soup.find("a", class_="paginacao-next")
    url = urljoin(url, next_button["href"]) if next_button else None

session.close()

df = pd.DataFrame(versicles)
df.to_csv("data/versicles.csv", index=False)

end = time.time()
time_taken = end - start
if time_taken > 120:
    minutes = time_taken // 60
    seconds = time_taken % 60
    print(f"Scraping completed in {int(minutes)} minutes and {seconds:.2f} seconds.")
else:
    print(f"Scraping completed in {time_taken:.2f} seconds.")