#!/usr/bin/python
import os
from dotenv import load_dotenv

load_dotenv()

## [LINKEDIN CREDENTIALS] ##
# it may be preferable to use a fake
# account to avoid account suspension

linkedin = dict(
    username = os.getenv("LI_USERNAME"),
    password = os.getenv("LI_PASSWORD"),
)

## [PROXY LIST] ##
# Leave empty to use your own IP address
# by using a proxy you can avoid being
# blocked for sending too much traffic

proxylist = []
#proxylist.append('http://127.0.0.1:8080')

## [MISCELLANEOUS] ##

timeout = 10
delay_hours = 48
daily_cap = 100
template_path = "templates/investor_intro.md"
