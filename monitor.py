"""
Collector Edition Monitor
-------------------------
Purpose:
    Monitors the official PlayStation Blog RSS feed for
    announcements mentioning special game editions.

Notifications:
    Sends matching new articles to a Discord webhook.

Requirements:
    Python 3
    DISCORD_WEBHOOK_URL environment variable

State:
    Stores previously seen article IDs in seen_posts.json.
"""


import json
import os
import re
import html
import urllib.request
import xml.etree.ElementTree as ET

FEED_URL = "https://blog.playstation.com/feed/"
STATE_FILE = "seen_posts.json"

KEYWORDS = [
    "collector's edition",
    "collectors edition",
    "collector edition",
    "limited edition",
    "deluxe edition",
    "ultimate edition",
    "premium edition",
    "special edition",
    "steelbook",
    "pre-order",
    "preorder",
    "pre order",
]


def get_feed():
    request = urllib.request.Request(
        FEED_URL,
        headers={"User-Agent": "CollectorEditionMonitor/1.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        content = response.read()

    root = ET.fromstring(content)
    posts = []

    for item in root.findall(".//item"):
        title = item.findtext("title", default="").strip()
        link = item.findtext("link", default="").strip()
        guid = item.findtext("guid", default=link).strip()
        description = item.findtext("description", default="")

        text = html.unescape(
            re.sub(r"<[^>]+>", " ", description)
        )

        posts.append({
            "id": guid or link or title,
            "title": title,
            "link": link,
            "text": text,
        })

    return posts


def load_seen():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as file:
            return set(json.load(file))
    except FileNotFoundError:
        return None


def save_seen(seen):
    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(sorted(seen), file, indent=2)


def send_discord(post):
    webhook = os.environ["DISCORD_WEBHOOK_URL"]

    message = (
        "🎮 **Possible PlayStation Edition Announcement!**\n"
        f"**{post['title']}**\n"
        f"{post['link']}"
    )

    payload = json.dumps({"content": message}).encode("utf-8")

    request = urllib.request.Request(
        webhook,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status not in (200, 204):
            raise RuntimeError("Discord notification failed")


def main():
    posts = get_feed()
    seen = load_seen()

    current_ids = {post["id"] for post in posts}

    # First run: establish a baseline without sending old alerts.
    if seen is None:
        save_seen(current_ids)
        print(f"Initial setup complete. Recorded {len(posts)} posts.")
        return

    new_matches = []

    for post in posts:
        searchable_text = (
            post["title"] + " " + post["text"]
        ).lower()

        matches = any(
            keyword in searchable_text for keyword in KEYWORDS
        )

        if post["id"] not in seen and matches:
            new_matches.append(post)

    for post in reversed(new_matches):
        send_discord(post)
        print(f"Notification sent: {post['title']}")

    save_seen(seen.union(current_ids))

    print(
        f"Check complete. {len(posts)} posts checked, "
        f"{len(new_matches)} new matching posts found."
    )


if __name__ == "__main__":
    main()
