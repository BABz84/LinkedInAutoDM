import os
import time
import json
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables from .env file
load_dotenv()

LI_USERNAME = os.getenv("LI_USERNAME")
LI_PASSWORD = os.getenv("LI_PASSWORD")

if not LI_USERNAME or not LI_PASSWORD:
    raise RuntimeError("LI_USERNAME and/or LI_PASSWORD not set in .env file")

# --- Selenium Driver Setup ---
driver = webdriver.Chrome()

def login_and_save_cookie():
    """
    Logs into LinkedIn using credentials from .env file,
    and saves the 'li_at' session cookie to a file.
    """
    print("Attempting to log in to LinkedIn...")
    driver.get("https://www.linkedin.com/login")

    try:
        # Wait for the username field to be visible and enter the username
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "session_key"))
        )
        username_field.send_keys(LI_USERNAME)

        # Enter the password
        password_field = driver.find_element(By.NAME, "session_password")
        password_field.send_keys(LI_PASSWORD)

        # Click the sign-in button
        driver.find_element(By.XPATH, '//*[@type="submit"]').click()

        # Wait for the login to complete by checking for a known element on the feed page
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "global-nav-search"))
        )

        print("Login successful.")

        # Get the 'li_at' cookie
        li_at_cookie = driver.get_cookie("li_at")
        if not li_at_cookie:
            raise RuntimeError("Could not find 'li_at' cookie after login.")

        # Get the 'JSESSIONID' cookie for the CSRF token
        csrf_cookie = driver.get_cookie("JSESSIONID")
        if not csrf_cookie:
            raise RuntimeError("Could not find 'JSESSIONID' cookie after login.")

        # Save the cookies to files
        with open("session.cookie", "w") as f:
            f.write(li_at_cookie['value'])
        
        # The actual CSRF token is the value of the JSESSIONID cookie, with quotes removed.
        csrf_token = csrf_cookie['value'].replace('"', '')
        with open("csrf.token", "w") as f:
            f.write(csrf_token)

        print("Session and CSRF tokens have been saved.")

    except Exception as e:
        print(f"An error occurred during login: {e}")
        print("Please check your credentials in the .env file and ensure the login page elements have not changed.")
    finally:
        driver.quit()

if __name__ == "__main__":
    login_and_save_cookie()
