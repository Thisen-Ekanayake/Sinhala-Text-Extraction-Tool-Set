import os
import requests
from bs4 import BeautifulSoup

# URL of the article
url = "https://sinhala.newsfirst.lk/2025/05/30/%E0%B7%83%E0%B7%94%E0%B7%85%E0%B6%82-%E0%B7%83%E0%B6%B8%E0%B6%9C-%E0%B7%80%E0%B7%90%E0%B7%83%E0%B7%92-%E0%B6%AD%E0%B6%AD%E0%B7%8A%E0%B6%AD%E0%B7%8A%E0%B7%80"

# Request page
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract title
title_tag = soup.find("h1", class_="top_stories_header_news")
title = title_tag.get_text(strip=True) if title_tag else "No Title Found"

# Extract date
date_tag = soup.find("div", class_="author_main")
date = date_tag.find("span").get_text(strip=True) if date_tag else "No Date Found"

# Extract article content
content_div = soup.find("div", class_="new_details")
paragraphs = content_div.find_all("p") if content_div else []
content = "\n".join(p.get_text(strip=True) for p in paragraphs)

# Folder to save articles
os.makedirs("newsfirst_articles", exist_ok=True)

# Generate file-safe name from title
filename = title.replace(" ", "_").replace(":", "").replace("|", "")[:50] + ".txt"
filepath = os.path.join("newsfirst_articles", filename)

# Save to file
with open(filepath, "w", encoding="utf-8") as f:
    f.write(f"Title: {title}\n")
    f.write(f"Date: {date}\n\n")
    f.write("Article:\n")
    f.write(content)

print(f"✅ Saved to {filepath}")
