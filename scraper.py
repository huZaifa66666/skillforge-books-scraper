#!/usr/bin/env python3
"""Collect book titles, prices, ratings, and availability from Books to Scrape.

Books to Scrape (https://books.toscrape.com/) is a demo website made for
practicing web scraping. Use this script only on sites you are permitted to
access, and follow the site's terms and robots.txt instructions.
"""

from __future__ import annotations

import argparse
import csv
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


@dataclass
class Book:
    title: str
    price: str
    rating: int
    availability: str
    product_url: str


class BooksToScrape:
    def __init__(self, delay: float = 0.5, timeout: int = 15) -> None:
        self.delay = max(0.0, delay)
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "SkillForgeLearningScraper/1.0 (educational demo)"}
        )

    def get_soup(self, url: str) -> BeautifulSoup:
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def scrape_page(self, url: str) -> tuple[list[Book], str | None]:
        soup = self.get_soup(url)
        books: list[Book] = []

        for item in soup.select("article.product_pod"):
            title_link = item.select_one("h3 a")
            price = item.select_one(".price_color")
            availability = item.select_one(".availability")
            rating_element = item.select_one("p.star-rating")

            if not all((title_link, price, availability, rating_element)):
                # Skip incomplete cards rather than failing the entire run.
                continue

            rating_class = next(
                (name for name in rating_element.get("class", []) if name in RATING_WORDS),
                None,
            )
            books.append(
                Book(
                    title=title_link.get("title", title_link.get_text(strip=True)),
                    price=price.get_text(strip=True),
                    rating=RATING_WORDS.get(rating_class or "", 0),
                    availability=" ".join(availability.get_text(" ", strip=True).split()),
                    product_url=urljoin(url, title_link.get("href", "")),
                )
            )

        next_link = soup.select_one("li.next a")
        next_url = urljoin(url, next_link["href"]) if next_link and next_link.get("href") else None
        return books, next_url

    def scrape(self, max_pages: int | None = None) -> list[Book]:
        current_url: str | None = BASE_URL
        all_books: list[Book] = []
        pages = 0

        while current_url and (max_pages is None or pages < max_pages):
            page_books, next_url = self.scrape_page(current_url)
            all_books.extend(page_books)
            pages += 1
            print(f"Page {pages}: collected {len(page_books)} books (total: {len(all_books)})")
            current_url = next_url
            if current_url and (max_pages is None or pages < max_pages):
                time.sleep(self.delay)

        return all_books


def save_csv(books: Iterable[Book], output: Path) -> int:
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = [asdict(book) for book in books]
    fieldnames = ["title", "price", "rating", "availability", "product_url"]
    with output.open("w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape book details from the Books to Scrape educational demo site."
    )
    parser.add_argument("--output", default="books.csv", help="Output CSV path (default: books.csv)")
    parser.add_argument("--max-pages", type=int, default=None, help="Maximum pages to scrape; omit for all pages")
    parser.add_argument("--delay", type=float, default=0.5, help="Seconds to wait between pages (default: 0.5)")
    args = parser.parse_args()

    if args.max_pages is not None and args.max_pages < 1:
        parser.error("--max-pages must be at least 1")
    if args.delay < 0:
        parser.error("--delay cannot be negative")

    try:
        scraper = BooksToScrape(delay=args.delay)
        books = scraper.scrape(max_pages=args.max_pages)
        count = save_csv(books, Path(args.output))
        print(f"Done. Saved {count} books to {args.output}")
    except requests.RequestException as exc:
        raise SystemExit(f"Network or HTTP error: {exc}") from exc


if __name__ == "__main__":
    main()
