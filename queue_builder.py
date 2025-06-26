#!/usr/bin/env python3
"""
Pull accepted connections from the LinkedIn UI, enqueue those older than DELAY_HOURS
"""
import time, datetime, config, db
import selenium.webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pathlib

def get_connections_from_ui(driver):
    """
    Navigates to the connections page and scrapes the list of connections.
    """
    print("Navigating to connections page to scrape connections...")
    driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
    
    connections = []
    try:
        # Wait for the initial connection list to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.scaffold-finite-scroll__content"))
        )
        print("Connection list container found. Starting scroll...")

        # New scrolling strategy based on research
        while True:
            # Get all currently loaded connection cards
            connection_cards = driver.find_elements(By.CSS_SELECTOR, ".mn-connection-card")
            if not connection_cards:
                print("No connection cards found.")
                break

            print(f"Found {len(connection_cards)} connection cards so far...")
            
            # Scroll to the last element to trigger loading more
            last_card = connection_cards[-1]
            actions = ActionChains(driver)
            actions.move_to_element(last_card).perform()
            
            # Wait for a moment to see if new cards load
            time.sleep(3)
            
            # Check if new cards have loaded
            new_connection_cards = driver.find_elements(By.CSS_SELECTOR, ".mn-connection-card")
            if len(new_connection_cards) == len(connection_cards):
                # No new cards loaded, we've reached the end
                print("Reached the end of the connections list.")
                break
        
        print("Finished scrolling. Scraping connection details...")
        all_cards = driver.find_elements(By.CSS_SELECTOR, ".mn-connection-card")
        print(f"Processing a total of {len(all_cards)} connection cards.")

        for card in all_cards:
            try:
                name_element = card.find_element(By.CSS_SELECTOR, ".mn-connection-card__name")
                profile_link_element = card.find_element(By.CSS_SELECTOR, ".mn-connection-card__link")
                
                name = name_element.text
                profile_url = profile_link_element.get_attribute("href")
                
                if '/in/' not in profile_url:
                    continue 
                    
                profile_id = profile_url.split('/in/')[1].split('/')[0]
                
                accepted_at = int(time.time())
                
                connections.append({"id": profile_id, "first_name": name.split()[0], "accepted_at": accepted_at})
            except Exception:
                continue

    except Exception as e:
        print(f"A critical error occurred while scraping connections: {e}")
        
    return connections

# --- Main Execution ---
try:
    li_at_cookie = pathlib.Path("session.cookie").read_text().strip()
except FileNotFoundError:
    raise RuntimeError("Session cookie not found. Please run auth.py first to log in.")

driver = wd.Chrome()
driver.get("https://www.linkedin.com")
driver.add_cookie({
    "name": "li_at",
    "value": li_at_cookie,
    "domain": ".linkedin.com"
})

conn = db.get_db_connection()
cur = conn.cursor()

scraped_connections = get_connections_from_ui(driver)
driver.quit()

for c in scraped_connections:
    cur.execute("INSERT OR IGNORE INTO connections VALUES (?,?,?)",
                   (c['id'], c['first_name'], c['accepted_at']))
conn.commit()

cutoff = int(time.time() - config.DELAY_HOURS * 3600)
cur.execute("""
  SELECT profile_id, first_name FROM connections
  WHERE accepted_at < ? AND profile_id NOT IN (SELECT profile_id FROM messages)
  ORDER BY accepted_at
  LIMIT ?
""", (cutoff, config.DAILY_CAP))
queue = cur.fetchall()
conn.close()

with open(".queue", "w") as f:
    for pid, name in queue:
        f.write(f"{pid},{name}\n")

print(f"Queue built with {len(queue)} contacts.")
