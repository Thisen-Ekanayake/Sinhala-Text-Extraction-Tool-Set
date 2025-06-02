"""import os
import time
import requests
from bs4 import BeautifulSoup

# Create output folder
output_folder = "itn_news_links"
os.makedirs(output_folder, exist_ok=True)

# Read sitemap links
with open("sitemap_links.txt", "r") as file:
    sitemap_urls = [line.strip() for line in file.readlines()]

# Process each sitemap with delay
for sitemap_url in sitemap_urls:
    try:
        print(f"[→] Processing: {sitemap_url}")
        response = requests.get(sitemap_url, timeout=10)
        response.raise_for_status()

        # Parse HTML structure
        soup = BeautifulSoup(response.content, "html.parser")
        all_links = soup.select("table#sitemap td a")

        filtered_links = []
        for a_tag in all_links:
            url = a_tag.get("href")
            if "/en/" not in url and "/ta/" not in url:
                filtered_links.append(url)

        # Save to file
        sitemap_name = sitemap_url.split("/")[-1].replace(".xml", "") + ".txt"
        output_path = os.path.join(output_folder, sitemap_name)

        with open(output_path, "w") as out_file:
            for link in filtered_links:
                out_file.write(link + "\n")

        print(f"[✓] Saved {len(filtered_links)} links to {output_path}")

    except Exception as e:
        print(f"[✗] Failed to process {sitemap_url}: {e}")

    # Delay to avoid hammering the server
    time.sleep(1.5)
"""


import os
import time
import requests
import xml.etree.ElementTree as ET

output_folder = "itn_news_links"
os.makedirs(output_folder, exist_ok=True)

sitemap_url = "https://www.itnnews.lk/post-sitemap2.xml"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36"
}

try:
    print(f"[→] Processing: {sitemap_url}")
    response = requests.get(sitemap_url, headers=headers, timeout=10)
    response.raise_for_status()

    # Parse XML directly
    root = ET.fromstring(response.content)

    # Extract URLs from <loc> tags
    filtered_links = []
    for url in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
        loc = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if loc is not None:
            link = loc.text
            if "/en/" not in link and "/ta/" not in link:
                filtered_links.append(link)

    # Save to file
    sitemap_name = sitemap_url.split("/")[-1].replace(".xml", "") + ".txt"
    output_path = os.path.join(output_folder, sitemap_name)

    with open(output_path, "w", encoding="utf-8") as out_file:
        for link in filtered_links:
            out_file.write(link + "\n")

    print(f"[✓] Saved {len(filtered_links)} links to {output_path}")

except Exception as e:
    print(f"[✗] Failed to process {sitemap_url}: {e}")

time.sleep(1.5)
