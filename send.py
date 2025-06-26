#!/usr/bin/env python3
import time, random, pathlib, sys
import selenium.webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import config, db
from datetime import datetime
import pytz

# --- Working Hours Check ---
tz = pytz.timezone(config.TIMEZONE)
current_hour = datetime.now(tz).hour
if not (config.WORKING_HOURS['start'] <= current_hour < config.WORKING_HOURS['end']):
    print(f"Outside of working hours ({config.WORKING_HOURS['start']}:00 - {config.WORKING_HOURS['end']}:00). Exiting.")
    exit()

queue = pathlib.Path(".queue").read_text().strip().splitlines()
if not queue:
    print("Queue is empty. Nothing to send.")
    exit()
template = pathlib.Path(config.TEMPLATE).read_text()

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

def human_sleep():
    """Sleep for a random duration to mimic human behavior."""
    time.sleep(random.uniform(30, 90))

def human_scroll(driver):
    """Scroll down the page to mimic human reading behavior."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.5);")
    time.sleep(random.uniform(1.5, 3.5))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(1.5, 3.5))


conn = db.get_db_connection()
cur = conn.cursor()

sent = 0
for line in queue:
    pid, name = line.split(",", 1)
    if sent >= config.DAILY_CAP:
        break
    try:
        print(f"[{sent+1}/{config.DAILY_CAP}] Processing profile: {pid}")
        driver.get(f"https://www.linkedin.com/in/{pid}/")

        if "checkpoint" in driver.current_url:
            print("LinkedIn security checkpoint detected. Halting execution.")
            status = "checkpoint_detected"
            cur.execute("INSERT OR REPLACE INTO messages VALUES (?,?,?)", (pid, int(time.time()), status))
            conn.commit()
            sys.exit() # Immediately stop the script

        human_scroll(driver)

        message_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'[aria-label="Message"]'))
        )
        message_button.click()

        message_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,'div.msg-form__contenteditable'))
        )
        
        msg = template.replace("{first}", name.split()[0])
        message_box.send_keys(msg)
        
        send_button = driver.find_element(By.CSS_SELECTOR,'button.msg-form__send-button')
        if not send_button.is_enabled():
            raise Exception("Send button is not enabled.")
        send_button.click()
        
        status = "ok"
        print(f"  Message sent successfully to {name}.")
        sent += 1
        
    except TimeoutException:
        status = "error:timeout"
        print(f"  Error: Timed out waiting for element on profile {pid}.")
    except NoSuchElementException:
        status = "error:no_element"
        print(f"  Error: Could not find a required element on profile {pid}.")
    except Exception as e:
        status = f"error:{e}".replace('\n', ' ').replace('\r', '')[:100]
        print(f"  An unexpected error occurred for profile {pid}: {e}")

    cur.execute("INSERT OR REPLACE INTO messages VALUES (?,?,?)",
                   (pid, int(time.time()), status))
    conn.commit()
    
    if status != "checkpoint_detected":
        human_sleep()

conn.close()
driver.quit()

# Generate the report after the run is complete
import reporter
reporter.generate_report()
