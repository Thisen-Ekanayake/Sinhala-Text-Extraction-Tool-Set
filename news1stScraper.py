import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import time
import random
import os

# === CONFIGURABLE RANGE ===
start_date = datetime.strptime("2025-01-01", "%Y-%m-%d")
end_date = datetime.strptime("2025-04-30", "%Y-%m-%d")

# === CONSTANTS ===
base_url = "https://sinhala.newsfirst.lk"
headers = {"User-Agent": "Mozilla/5.0"}
output_folder = "news_first_links_2025_04_30"

# === Create output folder if it doesn't exist ===
os.makedirs(output_folder, exist_ok=True)

# === LOOP THROUGH EACH DAY ===
current_date = start_date
while current_date <= end_date:
    year = current_date.strftime("%Y")
    month = current_date.strftime("%m")
    day = current_date.strftime("%d")

    # Build URL and regex for that day
    date_path = f"/{year}/{month}/{day}"
    url = base_url + date_path
    pattern = re.compile(rf"^/{year}/{month}/\d{{2}}/")  # auto match correct month/year
    filename = f"{year}-{month}-{day}_links.txt"
    filepath = os.path.join(output_folder, filename)

    print(f"🔍 Fetching: {url}")
    day_links = set()

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if pattern.match(href):
                full_url = base_url + href
                day_links.add(full_url)

        with open(filepath, "w", encoding="utf-8") as file:
            for link in sorted(day_links):
                file.write(link + "\n")

        print(f"✅ Saved {len(day_links)} links to {filepath}")

    except Exception as e:
        print(f"❌ Failed to fetch {url}: {e}")

    # Random delay to mimic human behavior
    delay = random.uniform(1.5, 3.5)
    print(f"⏳ Sleeping for {delay:.2f} seconds...\n")
    time.sleep(delay)

    current_date += timedelta(days=1)

print("🎉 Done! All daily links saved inside 'news_first_links' folder.")
