def generate_sitemap_links(start, end):
    links = []
    for i in range(start, end + 1):
        link = f"https://www.itnnews.lk/post-sitemap{i}.xml"
        links.append(link)
    return links

# Example usage
start = 1
end = 147  # Change this range as needed
sitemap_links = generate_sitemap_links(start, end)

# Save to a file (optional)
with open("sitemap_links.txt", "w") as file:
    for link in sitemap_links:
        file.write(link + "\n")

# Print to console
for link in sitemap_links:
    print(link)
