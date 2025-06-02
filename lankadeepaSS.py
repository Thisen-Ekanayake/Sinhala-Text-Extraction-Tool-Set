from playwright.sync_api import sync_playwright

def save_as_pdf(url, output_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto(url, timeout=60000)
        page.wait_for_load_state("networkidle")

        page.pdf(
            path=output_path,
            format="A4",
            landscape=False,
            display_header_footer=False,
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
            page_ranges="1-3"
        )

        print(f"✅ PDF saved to: {output_path}")
        browser.close()

url = "https://www.lankadeepa.lk/news/%E0%B6%85%E0%B6%B6%E0%B6%A9%E0%B6%B6-%E0%B6%AD%E0%B6%BD-%E0%B6%BD%E0%B6%9A%E0%B6%9A-%E0%B6%B6%E0%B6%BD%E0%B7%81%E0%B6%9A%E0%B6%AD-%E0%B6%87%E0%B6%B8%E0%B6%AD-%E0%B7%84%E0%B6%B8-%E0%B7%80%E0%B6%BA/101-673079"
output_pdf_path = "lankadeepa_article.pdf"

save_as_pdf(url, output_pdf_path)
