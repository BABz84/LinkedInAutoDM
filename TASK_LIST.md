# LinkedIn AutoDM Task List

This file tracks the required changes to implement the automated direct messaging feature.

## Task Checklist

- [x] **Add a `messages` table:**
    - `profile_id` TEXT PRIMARY KEY
    - `sent_at` TIMESTAMP

- [x] **Create a new script `queue_builder.py`:**
    - Hit `fs_connections`, filter `accepted_at >= 48h ago`, NOT IN `messages`.
    - Insert into `queue` table (`profile_id`, `first_name`, `accepted_at`).

- [x] **Extend `ScrapedIn.py` with a `send_dm(queue_row)` function:**
    - `driver.get(f"https://www.linkedin.com/in/{row.profile_id}")`
    - `driver.find_element(By.CSS_SELECTOR, '[aria-label="Message"]').click()`
    - `WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.msg-form__contenteditable'))).send_keys(TEMPLATE.format(first=row.first_name))`
    - `driver.find_element(By.CSS_SELECTOR, '[data-control-name="send"]').click()`
    - `cursor.execute("INSERT INTO messages VALUES (?, CURRENT_TIMESTAMP)", (row.profile_id, ))`
    - `random_sleep(45, 120)`

- [x] **Update `config.py`:**
    - Add `delay_hours`, `daily_cap`, and `template` text.

- [x] **Set up a Cron job:**
    - Run `queue_builder` at 03:00.
    - Run `ScrapedIn.py --mode send` at 03:30 every night.
