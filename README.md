# Books to Scrape — Beginner-Friendly Python Web Scraper

A small, documented Python project that demonstrates responsible web scraping against [Books to Scrape](https://books.toscrape.com/), a demo site designed for scraping practice.

## Features

- Collects book title, price, star rating, availability, and product URL
- Follows pagination automatically
- Exports results to a CSV file that opens in Excel
- Includes request timeouts, basic error handling, and a configurable delay
- Uses a `requests.Session` and readable, beginner-friendly code

## Requirements

- Python 3.10 or newer
- Internet connection

## Setup

### 1. Create and activate a virtual environment (recommended)

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the scraper

Scrape the first two pages and save the results to `books.csv`:

```bash
python scraper.py --max-pages 2 --output books.csv
```

Scrape all available pages:

```bash
python scraper.py --output books.csv
```

Optional arguments:

| Argument | Default | Purpose |
|---|---:|---|
| `--output` | `books.csv` | Output CSV file path |
| `--max-pages` | all pages | Limit the number of pages for a quick test |
| `--delay` | `0.5` | Seconds to wait between page requests |

Example with a slower delay:

```bash
python scraper.py --max-pages 3 --delay 1.0
```

## CSV columns

- `title` — book title
- `price` — displayed price as text
- `rating` — star rating from 1 to 5
- `availability` — displayed availability text
- `product_url` — absolute URL for the book's detail page

## Project structure

```text
skillforge-books-scraper/
├── scraper.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Responsible use

This repository is intended for learning with the Books to Scrape demo website. Before scraping any other website, check its terms, `robots.txt`, access rules, and applicable laws. Only collect data you are authorized to access. Keep request rates low, do not bypass logins or access controls, and stop if a site asks you to stop.

## Possible improvements

- Add automated tests
- Export to JSON as well as CSV
- Add structured logging
- Add a small command-line summary of average price and rating

## License

Released under the MIT License. See [`LICENSE`](LICENSE).
