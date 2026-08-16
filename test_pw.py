from playwright.sync_api import sync_playwright

def test_scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://hanzicraft.com/character/%E7%9A%84')
        page.wait_for_load_state('networkidle')
        
        print("Page Title:", page.title())
        
        # Let's find all text in the page to see if Breakdown and Components exist
        text = page.locator('body').inner_text()
        print("Body contains Breakdown:", "Breakdown" in text)
        print("Body contains Components:", "Components" in text)
        
        browser.close()

if __name__ == '__main__':
    test_scrape()
