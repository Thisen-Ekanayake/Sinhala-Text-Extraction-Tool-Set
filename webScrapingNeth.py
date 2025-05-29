import requests
from bs4 import BeautifulSoup
import os
import json
import time
import random

# === CONFIG ===
START_ID = 129001
END_ID = 135000
BATCH_SIZE = 100
DELAY_BETWEEN_BATCHES = 120  # 5 minutes
SAVE_DIR = "neth_articles_6000"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# === Setup ===
os.makedirs(SAVE_DIR, exist_ok=True)

def clean_text(text):
    return ' '.join(text.strip().split())

def scrape_article(article_id):
    url = f"https://www.nethnews.lk/article/{article_id}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[{article_id}] Skipped: Request error {e}")
        return

    soup = BeautifulSoup(response.content, "html.parser")

    title_tag = soup.find("h1", class_="entry-title")
    author_tag = soup.find("h4", class_="entry-title")
    date_tag = soup.find("time", class_="entry-date updated td-module-date")
    content_div = soup.find("div", class_="td-post-content")

    if not title_tag or not content_div:
        print(f"[{article_id}] Skipped: Missing title or content")
        return

    # Extract content from <p> tags only, skipping iframes, embeds, etc.
    content_paragraphs = []
    for p in content_div.find_all("p"):
        if p.find("iframe") or "Viber Group" in p.get_text():  # skip iframes or ads
            continue
        cleaned = clean_text(p.get_text())
        if cleaned:
            content_paragraphs.append(cleaned)

    content = "\n\n".join(content_paragraphs)
    title = clean_text(title_tag.get_text())
    author = clean_text(author_tag.get_text()) if author_tag else "Unknown"
    date = clean_text(date_tag.get_text()) if date_tag else "Unknown"

    # Save as .txt
    txt_path = os.path.join(SAVE_DIR, f"{article_id}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"{title}\n{author}\n{date}\n\n{content}")

    # Save as .json
    json_path = os.path.join(SAVE_DIR, f"{article_id}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "id": article_id,
            "url": url,
            "title": title,
            "author": author,
            "date": date,
            "content": content
        }, f, ensure_ascii=False, indent=2)

    print(f"[{article_id}] ✔️ Saved")

# === Run Scraper ===
for i, article_id in enumerate(range(START_ID, END_ID + 1), start=1):
    scrape_article(article_id)
    time.sleep(random.uniform(2, 4))  # short polite delay

    if i % BATCH_SIZE == 0 and article_id != END_ID:
        print(f"\n🕒 Batch {i // BATCH_SIZE} complete. Sleeping for {DELAY_BETWEEN_BATCHES // 60} minutes...\n")
        time.sleep(DELAY_BETWEEN_BATCHES)
