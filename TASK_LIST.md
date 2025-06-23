# LinkedIn AutoDM Task List

This file tracks the required changes to implement the automated direct messaging feature.

## Phase 1: Initial Implementation

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

## Phase 2: Enhancements

- [x] **Pull message copy into a file:**
    - Create a `templates` directory.
    - Create `templates/investor_intro.md`.
    - Update `config.py` to use `template_path`.

- [x] **Add a `messages` audit table:**
    - Add a `status` column to the `messages` table.
    - Update `queue_builder.py` to use a `LEFT JOIN` to avoid duplicates.

- [x] **Add a random-jitter helper:**
    - Create an `async def human_sleep(min_s=45, max_s=120)` function.

- [x] **Add a captcha/throttle detector:**
    - Look for URL patterns like `checkpoint/challenge` or HTTP 429.
    - Pause the bot and alert the user.

- [x] **Improve secrets hygiene:**
    - Add `.env.example` and `.gitignore`.
    - Use `python-dotenv` in `config.py`.

- [x] **Add a unit test for the delay filter:**
    - Create a `pytest` that seeds a dummy `accepted_at` 24h ago and expects **not** to enqueue.

## Phase 3: Advanced Features

- [x] **Import config in `queue_builder.py`**
- [x] **Cap the daily send volume**
- [x] **Reuse the Selenium session**
- [x] **Graceful pause after repeated captchas/throttles**
