# ***********************************************************
# Import libraries
# ***********************************************************
import ssl
import sqlite3
import requests
import traceback
import  pandas as pd
from io import StringIO  # Temporary write on RAM memory
from datetime import datetime


# ***********************************************************
# Code Block
# ***********************************************************
try:
    url_list = [
        'https://www.investing.com/commodities/real-time-futures',
        'https://en.wikipedia.org/wiki/Lists_of_countries_by_mineral_production',
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    all_tables_data = []

    for url_index, current_url in enumerate(url_list):
        print(f'Processing URL {url_index + 1}/{len(url_list)}: {current_url}')

        try:
            # Send request with header
            response = requests.get(current_url, headers=headers, verify=True)
            response.raise_for_status()

            # Automatic management of memory created with StringIO
            with StringIO(response.text) as buffer:
                # tables Return A list where each element is a data frame
                tables = pd.read_html(buffer)

            print(f'URL {url_index + 1}: The number of extracted tables: {len(tables)}')

            # Add URL info to each table
            for table_index, df in enumerate(tables):
                df["source_url"] = current_url
                df["url_index"] = url_index
                df["table_index"] = table_index
                df["extracted_at"] = datetime.now()
                all_tables_data.append(df)

        except Exception as url_error:
            print(f'Error processing URL {current_url}: {url_error}')
            continue

    print(f'Total tables extracted from all URLs: {len(all_tables_data)}')

    # Store to xlsx
    if all_tables_data:
        with pd.ExcelWriter("all_tables.xlsx") as writer:
            for idx, df in enumerate(all_tables_data, start=0):
                sheet_name = f"URL{df['url_index'].iloc[0]}_Table{df['table_index'].iloc[0]}"
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            print("Tables Saved to xlsx")
    else:
        print("No tables found to save to Excel")

    # Store in SQLite
    if all_tables_data:
        with sqlite3.connect("web_tables.db") as connection:
            cursor = connection.cursor()

            # First, delete all tables with url_table pattern in their name.
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'url_%_table_%'"
            )
            existing_tables = cursor.fetchall()
            for table in existing_tables:
                quoted_name = connection.execute(
                    "SELECT quote(?)", (table[0],)
                ).fetchone()[0]
                connection.execute(f"DROP TABLE IF EXISTS {quoted_name}")
            connection.commit()

            # Now save the new tables.
            for idx, df in enumerate(all_tables_data, start=0):
                table_name = f"url_{df['url_index'].iloc[0]}_table_{df['table_index'].iloc[0]}"
                df.to_sql(
                    name=table_name,
                    con=connection,
                    if_exists="replace",
                    index=False,
                )
            print(f"Tables Saved to database")
    else:
        print("No tables found to save to database")

except:
    print('Tables Not fount')
    print(traceback.print_exc())

