# Simple Web Scraper with Pandas

This project demonstrates a straightforward and efficient method for scraping tabular data from web pages using Python. Instead of relying on complex web scraping frameworks like Scrapy or BeautifulSoup, it leverages the powerful `pandas.read_html()` function to quickly extract HTML tables and store them in accessible formats.

The script is designed to be a practical tool for data analysts, scientists, and anyone who needs to quickly gather structured data from the web without a steep learning curve.

## 🚀 Key Features

- **Multi-URL Scraping**: Reads a list of URLs and scrapes tables from each one.
- **Metadata Enrichment**: Automatically adds metadata to each extracted table, including the source URL, a timestamp, and table/URL indices for better traceability.
- **Dual Storage Output**:
    1.  **Excel**: Saves all extracted tables into a single `.xlsx` file (`all_tables.xlsx`), with each table neatly organized in its own sheet.
    2.  **SQLite**: Stores each table in a local SQLite database (`web_tables.db`), making the data queryable and ready for further analysis.
- **Robust & Re-runnable**: Includes error handling for URLs that fail to load and intelligently cleans up old tables in the database before saving new ones, making the script safe to run multiple times.

## 🛠️ Prerequisites

- Python 3.10+
- The Python libraries listed in `requirements.txt`.

## ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ameri-mojtaba/web_scrapping_pandas
    cd web_scrapping_pandas

    ```

2.  **Install the required dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ How to Run

Simply execute the Python script from your terminal:

```bash
python web_scrapping_pandas.py

## 🤝 Connect with me 🤝

