from playwright.sync_api import sync_playwright
import time

def login_and_navigate():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Open login page
        page.goto("https://hiring.idenhq.com")

        # Enter credentials
        page.fill('input[type="email"]', "mamidi.anusha@cmr.edu.in")
        page.fill('input[type="password"]', "B60q6kMw")
        page.click('button:has-text("Sign in")')

        # Wait for the next page
        page.wait_for_url("https://hiring.idenhq.com/instructions")

        # Launch Challenge
        page.click('button:has-text("Launch Challenge")')
        page.wait_for_url("https://hiring.idenhq.com/challenge")

        # Open Menu and navigate to Inventory
        page.click('button:has-text("Menu")')
        page.click('text=Data Management')
        page.click('text=Inventory')

        # View All Products
        page.click('text=View All Products')
        page.wait_for_selector("text=Ready to view the complete product inventory?")

        # Wait for the Load Product Table button and click
        page.wait_for_selector('button:has-text("Load Product Table")', state="visible")
        time.sleep(2)  # Adding delay to ensure UI is ready
        page.click('button:has-text("Load Product Table")')

        # Wait for product table to load
        page.wait_for_selector("table.product-table")  # Adjust if needed

        print("Successfully loaded the Product Table!")
        browser.close()

# Run the script
login_and_navigate()
