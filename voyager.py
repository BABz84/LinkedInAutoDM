# voyager.py – minimal helper for LinkedIn Voyager (internal GraphQL) calls

from __future__ import annotations

import os
import time
import json
import pathlib
import requests
from typing import List, NamedTuple


class Connection(NamedTuple):
    id: str
    first_name: str
    accepted_at: int  # epoch seconds


# -- Configuration -------------------------------------------------------------
try:
    LI_AT = pathlib.Path("session.cookie").read_text().strip()
except FileNotFoundError:
    raise RuntimeError("Session cookie not found. Please run auth.py first to log in.")

# Load the CSRF token from the file saved by auth.py
try:
    CSRF = pathlib.Path("csrf.token").read_text().strip()
except FileNotFoundError:
    raise RuntimeError("CSRF token not found. Please run auth.py first to log in.")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "csrf-token": CSRF,
    "accept": "application/json",
    "Referer": "https://www.linkedin.com/feed/",
}

# This QUERY_ID is current as of June 2025.  Update if LinkedIn changes it.
QUERY_ID = "voyagerConnectionsDashConnections"

# How many rows per call (max is 50).
COUNT = 50


# -- Implementation ------------------------------------------------------------

def _voyager_session() -> requests.Session:
    """Return a pre‑cookie’d requests session ready for GraphQL calls."""
    sess = requests.Session()
    sess.headers.update(HEADERS)
    sess.cookies.set("li_at", LI_AT, domain=".linkedin.com")
    return sess


def _fetch_batch(session: requests.Session, start: int = 0) -> dict:
    url = (
        "https://www.linkedin.com/voyager/api/graphql?"
        f"variables={{'start':{start},'count':{COUNT}}}&"
        f"queryId={QUERY_ID}"
    )
    r = session.get(url)
    if r.status_code != 200:
        raise RuntimeError(f"Voyager error {r.status_code}: {r.text[:200]}")
    return r.json()


def get_accepted_connections() -> List[Connection]:
    """Return a *deduplicated* list of accepted connections."""
    sess = _voyager_session()
    batch = _fetch_batch(sess)

    # Voyager nests results in elements → items
    elements = batch.get("data", {}).get("voyagerConnectionsDashConnections", {}).get(
        "elements", []
    )
    connections: list[Connection] = []
    for e in elements:
        try:
            mini = e["miniProfile"]
            accepted_at = int(e.get("createdAt", 0) / 1000)
            connections.append(
                Connection(
                    id=mini["publicIdentifier"],
                    first_name=mini.get("firstName", ""),
                    accepted_at=accepted_at,
                )
            )
        except Exception:
            continue  # skip malformed rows

    # Dedup (shouldn’t be necessary but cheap)
    seen = set()
    unique: list[Connection] = []
    for c in connections:
        if c.id not in seen:
            unique.append(c)
            seen.add(c.id)
    return unique


# -- Manual test ---------------------------------------------------------------
if __name__ == "__main__":
    for c in get_accepted_connections()[:5]:
        t = time.strftime("%Y-%m-%d %H:%M", time.localtime(c.accepted_at))
        print(f"{c.id:25}  {c.first_name:15}  accepted {t}")
