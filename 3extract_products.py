from playwright.sync_api import sync_playwright
import json
import time

def scroll_and_load(page):
    """Scrolls down to load all products dynamically."""
    prev_count = 0
    while True:
        # Count number of loaded products
        product_cards = page.query_selector_all(".rounded-lg.border.bg-card")
        current_count = len(product_cards)
        
        if current_count == prev_count:  # No more new products are loading
            break
        
        prev_count = current_count
        print(f"🔄 Loaded {current_count} products, scrolling down...")
        
        # Scroll down to load more products
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)  # Wait for new products to load

    print(f"✅ All {current_count} products loaded!")

def extract_product_data(page):
    """Extracts all loaded product data."""
    products = []
    product_cards = page.query_selector_all(".rounded-lg.border.bg-card")

    for card in product_cards:
        try:
            name_element = card.query_selector("div.h-12")
            product_id_element = card.query_selector("div:nth-child(2) span.font-medium")
            details_element = card.query_selector("div:nth-child(3) span.font-medium")
            cost_element = card.query_selector("div:nth-child(4) span.font-medium")

            # Locate "Weight (kg)"
            weight_div = card.query_selector("div:has-text('Weight (kg)')")
            weight_element = weight_div.query_selector("span.font-medium:nth-child(2)") if weight_div else None

            # Extract text
            name = name_element.inner_text().strip() if name_element else "N/A"
            product_id = product_id_element.inner_text().strip() if product_id_element else "N/A"
            details = details_element.inner_text().strip() if details_element else "N/A"
            cost = cost_element.inner_text().strip() if cost_element else "N/A"
            weight = weight_element.inner_text().strip() if weight_element else "N/A"

            product_data = {
                "Product ID": product_id,
                "Name": name,
                "Details": details,
                "Cost": cost,
                "Weight (kg)": weight
            }

            products.append(product_data)
        except Exception as e:
            print(f"❌ Error extracting product: {e}")
            continue

    return products

def main():
    """Main function to extract all 4380 products."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Open login page
        page.goto("https://hiring.idenhq.com")
        page.wait_for_selector('input[type="email"]')

        # Enter credentials
        page.fill('input[type="email"]', "mamidi.anusha@cmr.edu.in")
        page.fill('input[type="password"]', "B60q6kMw")
        page.click('button:has-text("Sign in")')

        # Wait for page load
        page.wait_for_url("https://hiring.idenhq.com/instructions")

        # Launch Challenge
        page.click('button:has-text("Launch Challenge")')

        # Open inventory
        page.click('button:has-text("Menu")')
        page.click('text=Data Management')
        page.click('text=Inventory')

        # View All Products
        page.click('text=View All Products')
        page.wait_for_selector("text=Ready to view the complete product inventory?")

        # Click "Load Product Table"
        page.wait_for_selector('button:has-text("Load Product Table")', state="visible")
        page.click('button:has-text("Load Product Table")')
        time.sleep(3)  # Wait for initial products to load

        # Scroll down to load all products
        scroll_and_load(page)

        # Extract product data
        all_products = extract_product_data(page)

        # Save data
        with open("products.json", "w", encoding="utf-8") as f:
            json.dump(all_products, f, indent=4)

        print(f"\n✅ Extracted {len(all_products)} products and saved to 'products.json'!")

        browser.close()

if __name__ == "__main__":
    main()
