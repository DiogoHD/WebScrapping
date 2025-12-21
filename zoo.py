import requests
from bs4 import BeautifulSoup

res = requests.get("https://www.zoo.pt/pt/conhecer/animais/animais-de-a-a-z/")
soup = BeautifulSoup(res.content, "lxml")

animal_boxes = soup.select("div.animalBox")
animal_links = [box.find("a")["href"] for box in animal_boxes]

for link in animal_links:
    print(link)