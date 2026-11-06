
"""
Collector Edition Monitor - brack diagnostic
Purpose:
    Inspects brack's Collector's Edition category page.

This is a diagnostic tool, not the final stock monitor.
It checks whether product information is accessible
to the automated monitoring system.
"""

import urllib.request
from html.parser import HTMLParser

URL = "https://www.brack.ch/


class PageInspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title_text = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "title":
            self.in_title = True

        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_text.append(data)


def main():
    request = urllib.request.Request(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0 CollectorEditionMonitor/1.0"
        }
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        page = response.read().decode("utf-8", errors="replace")

        print("HTTP status:", response.status)
        print("Final URL:", response.url)
        print("Downloaded characters:", len(page))

    inspector = PageInspector()
    inspector.feed(page)

    print("Page title:", "".join(inspector.title_text))
    print("Collector keyword present:", "collector" in page.lower())
    print("Steelbook keyword present:", "steelbook" in page.lower())

    print("\nFirst 20 links:")
    for link in inspector.links[:20]:
        print(link)


if __name__ == "__main__":
    main()
