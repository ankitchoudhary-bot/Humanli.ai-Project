import requests
from bs4 import BeautifulSoup, Tag
from readability import Document
from urllib.parse import urlparse
import re
import hashlib
from typing import Optional

# Configuration
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

TIMEOUT = 10
MIN_TEXT_LENGTH = 200

# Custom Exceptions
class ScraperError(Exception):
    pass

# Utility Functions
def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)

def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def hash_text(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()

# Core Scraper
class HTMLContentScraper:
    def __init__(self, url: str):
        self.url = url
        self.html: Optional[str] = None
        self.soup: Optional[BeautifulSoup] = None

    # Step 1: Fetch HTML
    def fetch(self):
        if not is_valid_url(self.url):
            raise ScraperError("Invalid URL format")

        try:
            response = requests.get(
                self.url,
                headers=HEADERS,
                timeout=TIMEOUT,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise ScraperError(f"Request failed: {e}")

        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            raise ScraperError("Unsupported content type (not HTML)")

        self.html = response.text

    # Step 2: Extract main article (Readability)
    def extract_main_html(self):
        doc = Document(self.html)
        clean_html = doc.summary(html_partial=True)
        self.soup = BeautifulSoup(clean_html, "lxml")

    # Step 3: Remove unwanted sections
    def remove_irrelevant_sections(self):
        REMOVE_TAGS = [
            "header",
            "footer",
            "nav",
            "aside",
            "form",
            "iframe",
            "noscript",
            "script",
            "style",
        ]

        REMOVE_ROLES = [
            "navigation",
            "banner",
            "contentinfo",
            "complementary",
            "advertisement",
        ]

        # Remove by tag name
        for tag in REMOVE_TAGS:
            for el in self.soup.find_all(tag):
                el.decompose()

        # Remove ads / nav by role or class/id keywords
        to_remove = []

        for el in self.soup.find_all(True):
            if not hasattr(el, "attrs") or el.attrs is None:
                continue

            role = el.attrs.get("role", "")
            class_id = " ".join(el.attrs.get("class", [])) + " " + (el.attrs.get("id") or "")

            if role in REMOVE_ROLES or re.search(
                r"ad-|ads|advert|promo|sidebar|cookie|popup", class_id, re.I
            ):
                to_remove.append(el)

        for el in to_remove:
            el.decompose()

    # Step 4: Extract & deduplicate text
    def extract_clean_text(self) -> str:
        paragraphs = self.soup.find_all(["p", "li", "article", "section"])

        seen_hashes = set()
        clean_blocks = []

        for p in paragraphs:
            text = normalize_text(p.get_text(" ", strip=True))

            if len(text) < 40:
                continue

            h = hash_text(text)
            if h not in seen_hashes:
                seen_hashes.add(h)
                clean_blocks.append(text)

        final_text = "\n\n".join(clean_blocks)

        if len(final_text) < MIN_TEXT_LENGTH:
            raise ScraperError("No meaningful content found")

        return final_text

    # Public API
    def scrape(self) -> str:
        self.fetch()
        self.extract_main_html()
        self.remove_irrelevant_sections()
        return self.extract_clean_text()

# Entry Point
def scrape_url(url: str) -> str:
    scraper = HTMLContentScraper(url)
    return scraper.scrape()

# # Example Usage
# if __name__ == "__main__":
#     url = "https://en.wikipedia.org/wiki/Web_scraping"

#     try:
#         content = scrape_url(url)
#         save_text_to_pdf(
#             text=content,
#             filename="web_scraping_article.pdf"
#         )

#         print("PDF saved successfully!")

        
#     except ScraperError as e:
#         print("Error:", e)

