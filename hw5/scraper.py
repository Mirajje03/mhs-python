import asyncio
import aiohttp
import json
import os
from bs4 import BeautifulSoup

HISTORY_FILE = "cian_history.json"
CHECK_INTERVAL = 60

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_history(data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def parse_cian_page(session):
    url = "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&region=1&room1=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                print(f"Error: Status code {response.status}")
                return []
            
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            
            ads = []
            
            cards = soup.find_all("article", {"data-name": "CardComponent"})
            
            for card in cards:
                try:
                    link_tag = card.find("a", href=True)
                    link = link_tag['href'] if link_tag else "No link"
                    
                    price_tag = card.find("span", {"data-mark": "MainPrice"})
                    price = price_tag.get_text(strip=True) if price_tag else "No price"
                    
                    title_tag = card.find("span", {"data-mark": "OfferTitle"})
                    title = title_tag.get_text(strip=True) if title_tag else "No title"

                    ad_data = {
                        "id": link,
                        "title": title,
                        "price": price,
                        "link": link
                    }
                    ads.append(ad_data)
                except Exception:
                    continue
            
            return ads

    except Exception as e:
        print(f"Connection error: {e}")
        return []

async def worker():
    print("Scraper started. Press Ctrl+C to stop.")
    
    while True:
        existing_data = load_history()
        existing_ids = {item["id"].split('/')[4] for item in existing_data}
        
        async with aiohttp.ClientSession() as session:
            new_ads = await parse_cian_page(session)
        
        fresh_finds = []
        for ad in new_ads:
            if ad["id"].split('/')[4] not in existing_ids:
                fresh_finds.append(ad)
                existing_data.append(ad)
        
        if fresh_finds:
            print(f"Found {len(fresh_finds)} new ads!")
            for item in fresh_finds:
                print(f"- {item['title']} : {item['price']}")
            
            save_history(existing_data)
        else:
            print("No new ads found.")
        
        print(f"Waiting {CHECK_INTERVAL} seconds...")
        await asyncio.sleep(CHECK_INTERVAL)

async def main():
    await worker()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nScraper stopped.")
