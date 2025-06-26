# --- General Configuration ---

# The path to the message template you want to send.
# You can create multiple templates in the /templates/ directory.
TEMPLATE = "templates/investor_intro.md"

# --- Throttling Configuration ---

# The bot will not send a message to a new connection
# until at least this many hours have passed.
DELAY_HOURS = 48

# The maximum number of messages the bot will send in a single day.
DAILY_CAP = 25

# --- "Human-Like" Behavior Configuration ---

# To avoid detection, the bot will only run during these hours.
# Use 24-hour format (e.g., 9 for 9 AM, 17 for 5 PM).
WORKING_HOURS = {"start": 9, "end": 23}

# Set your local timezone.
# A list of valid timezones can be found here:
# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TIMEZONE = "America/Chicago"
