from playwright.sync_api import sync_playwright
import os

# Define the session file path
SESSION_FILE = "session.json"
LOGIN_URL = "https://hiring.idenhq.com"

def check_or_login(playwright):
    browser = playwright.chromium.launch(headless=False)  # Set headless=True if running in the background
    context = None

    # Check if session file exists
    if os.path.exists(SESSION_FILE):
        print("Session found. Using saved session.")
        context = browser.new_context(storage_state=SESSION_FILE)
    else:
        print("No session found. Logging in...")
        context = browser.new_context()
        page = context.new_page()
        page.goto(LOGIN_URL)

        # Enter credentials
        page.fill("input[type='email']", "your_email@example.com")
        page.fill("input[type='password']", "your_password")
        page.click("button:has-text('Sign in')")

        # Wait for successful login (adjust selector based on what appears after login)
        page.wait_for_selector("text=Dashboard", timeout=10000)  # Modify this according to the actual dashboard selector
        
        # Save session state
        context.storage_state(path=SESSION_FILE)
        print("Session saved successfully.")

    return context, browser

with sync_playwright() as playwright:
    context, browser = check_or_login(playwright)
    browser.close()
