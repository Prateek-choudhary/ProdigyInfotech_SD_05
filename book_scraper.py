import requests
from bs4 import BeautifulSoup
import pandas as pd


URL = "https://books.toscrape.com/catalogue/page-{}.html"


rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


products = []


for page in range(1, 3): 
    print(f"📄 Scraping page {page}...")

    response = requests.get(URL.format(page))
    soup = BeautifulSoup(response.content, "html.parser")

    articles = soup.find_all("article", class_="product_pod")

    for article in articles:
        title = article.h3.a["title"]
        price = article.find("p", class_="price_color").text.strip()
        rating_class = article.find("p", class_="star-rating")["class"][1]
        rating = rating_map.get(rating_class, 0)

        products.append({
            "Title": title,
            "Price": price,
            "Rating": rating
        })


df = pd.DataFrame(products)
df.to_csv("books.csv", index=False)

print("✅ Scraping completed. Data saved to books.csv")
