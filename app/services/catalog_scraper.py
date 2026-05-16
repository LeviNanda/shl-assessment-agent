import json
import time
from pathlib import Path
from typing import List, Dict
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.shl.com/products/product-catalog/"
DATA_PATH = Path("app/data/catalog.json")


def clean_text(text: str) -> str:
    return " ".join(text.replace("\n", " ").replace("\t", " ").split())


def scrape_catalog_page(start: int = 0) -> List[Dict]:
    url = f"{BASE_URL}?start={start}&type=1"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("tr")

    products = []

    for row in rows:
        link = row.select_one("a[href]")
        if not link:
            continue

        name = clean_text(link.get_text())
        href = link.get("href")

        if not name or "product-catalog" not in href:
            continue

        if href.startswith("/"):
            product_url = "https://www.shl.com" + href
        else:
            product_url = href

        cells = [clean_text(cell.get_text()) for cell in row.select("td")]

        product = {
            "name": name,
            "url": product_url,
            "test_type": "",
            "description": " ".join(cells),
            "raw_text": clean_text(row.get_text(" "))
        }

        products.append(product)

    return products


def scrape_all_catalog() -> List[Dict]:
    all_products = []
    seen_urls = set()

    for start in range(0, 1000, 12):
        print(f"Scraping start={start}...")

        try:
            products = scrape_catalog_page(start)
        except Exception as e:
            print(f"Failed at start={start}: {e}")
            break

        new_count = 0

        for product in products:
            if product["url"] not in seen_urls:
                seen_urls.add(product["url"])
                all_products.append(product)
                new_count += 1

        if new_count == 0:
            break

        time.sleep(1)

    return all_products


def save_catalog():
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    products = scrape_all_catalog()

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(products)} products to {DATA_PATH}")


if __name__ == "__main__":
    save_catalog()