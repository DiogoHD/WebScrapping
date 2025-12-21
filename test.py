import requests
from bs4 import BeautifulSoup

res = requests.get("https://www.zoo.pt/sitemap.xml")
soup = BeautifulSoup(res.content, "lxml")

urls = [loc.text for loc in soup.find_all("loc")]
urls_animals = [url for url in urls if "/animais/" in url]
mamifers_urls = [url for url in urls_animals if "/mamiferos/" in url]
aves_urls = [url for url in urls_animals if "/aves/" in url]
repteis_urls = [url for url in urls_animals if "/repteis/" in url]
anfibios_urls = [url for url in urls_animals if "/anfibios-e-outros/" in url]

print("Mamíferos URLs: " + str(len(mamifers_urls)))
for url in mamifers_urls:
    print(url)

print("\nAves URLs: " + str(len(aves_urls)))
for url in aves_urls:
    print(url)

print("\nRépteis URLs: " + str(len(repteis_urls)))
for url in repteis_urls:
    print(url)
print("\nAnfíbios e Outros URLs: " + str(len(anfibios_urls)))
for url in anfibios_urls:
    print(url)