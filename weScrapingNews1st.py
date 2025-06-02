import os
import requests
from bs4 import BeautifulSoup
import json
import time
import random

def extract_news_from_url(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract title
            title_tag = soup.find("h1", class_="top_stories_header_news")
            title = title_tag.get_text(strip=True) if title_tag else "No Title Found"

            # Extract date
            date_tag = soup.find("div", class_="author_main")
            date = date_tag.find("span").get_text(strip=True) if date_tag else "No Date Found"

            # Extract full article content from <div class="new_details">
            content_div = soup.find("div", class_="new_details")
            if content_div:
                content = content_div.get_text(separator="\n", strip=True)
            else:
                content = "No Content Found"

            return {"title": title, "date": date, "content": content, "url": url}

        except Exception as e:
            print(f"Attempt {attempt+1} failed for url: {e}")
            time.sleep(1.5)

    return None


def extract_from_folder(folder_name):
    folder_path = os.path.join(os.getcwd(), folder_name)
    if not os.path.exists(folder_path):
        print("❌ Folder does not exist.")
        return

    output_folder = os.path.join(folder_path, "extracted_news")
    os.makedirs(output_folder, exist_ok=True)

    file_counter = 1
    seen_urls = set()

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                for line in file:
                    url = line.strip()
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        
                        print(f"🔍 Processing: url")
                        news_data = extract_news_from_url(url)
                        
                        if news_data:
                            file_id = f"{file_counter:02}"
                            txt_path = os.path.join(output_folder, f"{file_id}.txt")
                            json_path = os.path.join(output_folder, f"{file_id}.json")

                            with open(txt_path, "w", encoding="utf-8") as txt_file:
                                txt_file.write(f"{news_data['title']}\n{news_data['date']}\n\n{news_data['content']}")

                            with open(json_path, "w", encoding="utf-8") as json_file:
                                json.dump(news_data, json_file, ensure_ascii=False, indent=4)

                            print(f"✅ Saved: {file_id}.txt / .json")
                            file_counter += 1
                        else:
                            print(f"❗ Failed after retries:")

                        # Random delay to mimic human behavior
                        time.sleep(random.uniform(1, 2))
                    elif url in seen_urls:
                        print(f"⏩ Skipped duplicate: {url}")

# 👇 Run the extractor
if __name__ == "__main__":
    folder_name = input("📁 Enter the folder name (inside current directory): ")
    extract_from_folder(folder_name)
