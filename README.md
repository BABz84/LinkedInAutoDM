# LinkedIn Auto-Messenger

**Objective:** A tool to automatically send personalized direct messages to your LinkedIn connections. This tool is intended for efficient and targeted outreach.

**NOTE:** This tool is designed to interact with the LinkedIn website in a way that mimics human behavior to reduce the risk of account suspension. However, any form of automation is against the LinkedIn Terms of Service. Use this tool responsibly and at your own risk.

---

## 1. Installation

To get started, you need Python 3 and pip installed.

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd LinkedInAutoDM
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 2. Configuration

The application requires credentials and other settings to be configured in a `.env` file.

1.  **Create the environment file:**
    Make a copy of the example file and name it `.env`:
    ```bash
    cp .env.example .env
    ```

2.  **Edit the `.env` file:**
    Open the `.env` file in a text editor and add your LinkedIn credentials:
    ```
    LI_USERNAME="your_linkedin_email@example.com"
    LI_PASSWORD="your_linkedin_password"
    ```

---

## 3. Getting Started: First-Time Setup

Before you can send messages, you need to perform these two one-time setup steps:

1.  **Create the Database:**
    This command creates the `data.sqlite3` file that will track your messaging activity.
    ```bash
    python db.py
    ```

2.  **Log In to LinkedIn:**
    This command will open a browser and ask you to log in. After a successful login, it will save a session cookie so you don't have to log in again.
    ```bash
    python auth.py
    ```

## 4. Regular Use

Once you have completed the setup, you only need to run these two commands to send messages:

1.  **Build the Message Queue:**
    ```bash
    python queue_builder.py
    ```

2.  **Send Messages:**
    ```bash
    python send.py
    ```

---
## 5. Customizing Your Message

You can create and use different message templates.

1.  **Create a new template:**
    Add a new `.md` file in the `/templates` directory. You can use `{first}` as a placeholder for the contact's first name.

2.  **Select the template:**
    Open `config.py` and change the `TEMPLATE` variable to point to your new file.
    ```python
    TEMPLATE = "templates/your_new_template.md"
    ```

---

## Sponsorship
[<img src="proxycurl.png" width=350>](https://nubela.co/proxycurl?utm_campaign=influencer_marketing&utm_source=github&utm_medium=social&utm_content=daniel_chrastil_scrapedin)

> Scrape public LinkedIn profile data at scale with [Proxycurl APIs](https://nubela.co/proxycurl?utm_campaign=influencer_marketing&utm_source=github&utm_medium=social&utm_content=daniel_chrastil_scrapedin).
> - Scraping Public profiles are battle-tested in court in HiQ VS LinkedIn case.
> - GDPR, CCPA, SOC2 compliant
> - High rate Limit - 300 requests/minute
> - Fast APIs respond in ~2s
> - Fresh data - 88% of data is scraped real-time, other 12% are not older than 29 days
> - High accuracy
> - Tons of data points returned per profile
>
> Built for developers, by developers.

### Disclaimer
This tool is for educational purposes only. Automating interactions on LinkedIn violates their Terms of Service. Use this tool responsibly and at your own risk. The developers are not responsible for any consequences of using this software, including but not limited to account suspension or termination.
