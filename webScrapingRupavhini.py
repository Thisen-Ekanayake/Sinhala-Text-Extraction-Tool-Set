import requests
from bs4 import BeautifulSoup
import time
import random
import json
import os

# Create output folders
os.makedirs("news_json", exist_ok=True)
os.makedirs("news_txt", exist_ok=True)

# Load the XML sitemap
sitemap_url = "https://rupavahininews.lk/wp-sitemap-posts-post-1.xml"
response = requests.get(sitemap_url)
soup = BeautifulSoup(response.content, 'xml')

# Extract post URLs
post_urls = [loc.text for loc in soup.find_all('loc')]

# Extract data from each post
def extract_news_details(url):
    try:
        res = requests.get(url, timeout=10)
        page = BeautifulSoup(res.content, 'html.parser')
        
        title = page.find('h1', class_='entry-title').text.strip()
        date = page.find('div', class_='date').text.strip()
        author = page.find('div', class_='by-author').text.strip()
        content_div = page.find('div', class_='entry-content')
        content = "\n".join(p.text.strip() for p in content_div.find_all('p') if p.text.strip())

        return {
            "url": url,
            "title": title,
            "date": date,
            "author": author,
            "content": content
        }
    except Exception as e:
        print(f"❌ Error processing {url}: {e}")
        return None

# Loop through URLs and save each article separately
for i, url in enumerate(post_urls, start=1):
    print(f"🔄 Processing ({i}/{len(post_urls)}): {url}")
    news = extract_news_details(url)
    if news:
        file_id = f"{i:02d}"  # zero-padded index

        # Save JSON
        json_filename = f"news_json/rupavahini_news_{file_id}.json"
        with open(json_filename, "w", encoding='utf-8') as f_json:
            json.dump(news, f_json, ensure_ascii=False, indent=2)

        # Save TXT
        txt_filename = f"news_txt/rupavahini_news_{file_id}.txt"
        with open(txt_filename, "w", encoding='utf-8') as f_txt:
            f_txt.write(f"📰 Title: {news['title']}\n")
            f_txt.write(f"📅 Date: {news['date']}\n")
            f_txt.write(f"✍️ Author: {news['author']}\n")
            f_txt.write(f"🔗 URL: {news['url']}\n\n")
            f_txt.write(f"{news['content']}\n")

    time.sleep(random.uniform(1, 3))  # Delay to mimic real user

print("\n✅ Done. Each article saved in:")
print("📁 news_json/ (JSON format)")
print("📁 news_txt/ (Plain text format)")
