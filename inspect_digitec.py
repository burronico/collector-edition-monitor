
"""
Collector Edition Monitor - Digitec diagnostic
Purpose:
    Inspects Digitec's Collector's Edition category page.

This is a diagnostic tool, not the final stock monitor.
It checks whether product information is accessible
to the automated monitoring system.
"""

import urllib.request
from html.parser import HTMLParser

URL = (
    "https://www.digitec.ch/en/s1/producttype/"
    "video-games-46/filter/edition-collectors-edition-88810"
)


class PageInspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = False
        self.title_text = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "title":
            self.title = True

        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])

    def handle_endtag(self, tag):
        if tag == "title":
            self.title = False

    def handle_data(self, data):
        if self.title:
            self.title_text.append(data)


def main():
    request = urllib.request.Request(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0 CollectorEditionMonitor/1.0"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            html = response.read().decode("utf-8", errors="replace")

            print("HTTP status:", response.status)
            print("Final URL:", response.url)
            print("Downloaded characters:", len(html))

    except Exception as error:
        print("Could not retrieve Digitec:", error)
        raise

    inspector = PageInspector()
    inspector.feed(html)

    print("Page title:", "".join(inspector.title_text))
    print("Collector keyword present:", "collector" in html.lower())

    product_links = [
        link for link in inspector.links
        if "/product/" in link
    ]

    print("Product links found:", len(product_links))

    print("\nFirst 10 product links:")
    for link in product_links[:10]:
        print(link)


if __name__ == "__main__":
    main()
