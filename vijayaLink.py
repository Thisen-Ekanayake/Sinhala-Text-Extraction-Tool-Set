import requests
from bs4 import BeautifulSoup

# Target URL
url = "https://www.wijeya.lk/world/212"

# Headers to mimic a real browser
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Send GET request with headers
response = requests.get(url, headers=HEADERS)
response.raise_for_status()

# Parse HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Find all divs with class "col-md-7"
divs = soup.find_all("div", class_="col-md-7")

# Extract hrefs
links = []
for div in divs:
    a_tag = div.find("a", href=True)
    if a_tag:
        links.append(a_tag['href'])

# Save to file
with open("vijaya_links_2.txt", "w", encoding="utf-8") as f:
    for link in links:
        f.write(link + "\n")

print(f"✅ Extracted {len(links)} links and saved to links.txt")
