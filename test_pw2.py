from playwright.sync_api import sync_playwright

def test_scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://hanzicraft.com/character/%E7%9A%84', wait_until='domcontentloaded')
        
        try:
            page.wait_for_selector('text=Breakdown', timeout=5000)
        except Exception as e:
            print("Could not find Breakdown text:", e)
            
        with open('body.html', 'w', encoding='utf-8') as f:
            f.write(page.content())
            
        browser.close()

if __name__ == '__main__':
    test_scrape()
