import pandas as pd
import requests
import os
import re
import json
import time
import random
import numpy as np
from io import StringIO
from bs4 import BeautifulSoup

# --- 1. Helper Function ---
def get_clean_filename(text, index=None):
    # Remove non-alphanumeric characters and split by whitespace
    words = re.sub(r'[^a-zA-Z0-9\s]', '', text).split()
    if not words:
        base_name = "scrapedData"
    else:
        # lowercase first word, capitalize subsequent words
        base_name = words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    
    # Add index suffix if multiple tables are found to avoid overwriting
    suffix = f"_{index}" if index is not None else ""
    return f"{base_name}{suffix}.json"

# --- 2. Setup ---
# Thresholds for a valid table
MIN_ROWS = 10
MIN_COLS = 4
headers = {'User-Agent': 'Mozilla/5.0'}
CANDIDATES_FILE = "./candidateTables.txt"
OUTPUT_DIR = "./tables"

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- 3. User Input & Mode Selection ---
user_input = input("Enter a Wikipedia URL (or press Enter to use a random one from candidateTables.txt): ").strip()

if user_input:
    target_urls = [user_input]
    is_random = False
    print(f"🎯 Target Mode: Attempting to scrape {user_input}...")
else:
    is_random = True
    if os.path.exists(CANDIDATES_FILE):
        with open(CANDIDATES_FILE, 'r', encoding='utf-8') as f:
            # Convert lines to full Wikipedia URLs
            lines = [line.strip() for line in f if line.strip()]
            # Shuffle the list to choose a random starting point
            random.shuffle(lines)
            target_urls = [f"https://en.wikipedia.org/wiki/{line}" for line in lines]
        print(f"📂 Shuffle Mode: Searching through curated articles in random order...")
    else:
        print(f"🚨 Error: {CANDIDATES_FILE} not found. Please create the file or enter a URL.")
        target_urls = []

# --- 4. Main Scraping Loop ---
found_any_eligible_page = False

for url_index, target_url in enumerate(target_urls):
    # If we are in random mode and found a page with tables, we can stop searching.
    # If we are in target mode, we only have one URL anyway.
    if is_random and found_any_eligible_page:
        break
        
    attempts = url_index + 1
    if is_random:
        print(f"\n--- Article #{attempts}: {target_url.split('/')[-1]} ---")
    
    try:
        response = requests.get(target_url, headers=headers, timeout=10)
        final_url = response.url 
        soup = BeautifulSoup(response.text, 'html5lib')

        # Extract article name
        article_name = soup.title.string.replace(" - Wikipedia", "") if soup.title else "Unknown Article"
        print(f"Checking: '{article_name}'")

        # --- Parse & Clean Table ---
        html_data = StringIO(response.text)
        try:
            # Using flavor 'bs4' for more robust table identification
            tables = pd.read_html(html_data, flavor='bs4')
        except ValueError:
            tables = []

        if not tables:
            print("❌ No tables found in this article.")
            continue

        table_stats = []
        eligible_tables_on_page = []
        
        # First pass: Identify all eligible tables
        for i, df in enumerate(tables):
            rows, cols = df.shape
            if rows >= MIN_ROWS and cols >= MIN_COLS:
                eligible_tables_on_page.append((i, df))
            else:
                table_stats.append(f"T{i+1}: Small ({rows}x{cols})")

        if not eligible_tables_on_page:
            print(f"⚠️ No eligible tables: {', '.join(table_stats)}")
            if is_random:
                time.sleep(0.5)
            continue

        # Second pass: Process and save eligible tables
        found_any_eligible_page = True
        for count, (original_index, df) in enumerate(eligible_tables_on_page):
            # Flatten headers if nested
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(-1)
            
            # Ensure column names are unique
            if df.columns.duplicated().any():
                df.columns = [f"{c}_{idx}" if duplicated else c 
                             for idx, (c, duplicated) in enumerate(zip(df.columns, df.columns.duplicated()))]

            # Clean citations [1], [a] and extra whitespace
            def clean_text(val):
                if isinstance(val, str):
                    return re.sub(r'\[.*?\]', '', val).strip()
                return val

            df = df.map(clean_text)

            # --- 5. Column Analysis ---
            column_types = {}
            for col in df.columns:
                series = df[col]
                if isinstance(series, pd.DataFrame):
                    series = series.iloc[:, 0]
                
                test_col = series.astype(str).str.replace(r'[$,%]', '', regex=True)
                converted = pd.to_numeric(test_col, errors='coerce')
                
                if converted.notna().mean() > 0.5:
                    column_types[col] = "quantitative"
                else:
                    column_types[col] = "qualitative"

            # --- 6. JSON Safety Check ---
            # Replace NaN with None so it becomes 'null' in the resulting JSON
            df_json_ready = df.replace({np.nan: None})
            records = df_json_ready.to_dict(orient='records')

            final_output = {
                "metadata": {
                    "source_url": final_url,
                    "article_name": article_name,
                    "table_index": original_index + 1,
                    "row_count": len(records),
                    "column_count": len(df.columns),
                    "column_analysis": column_types,
                    "attempts_made": attempts,
                    "mode": "random_candidate" if is_random else "target"
                },
                "data": records
            }

            # --- 7. Save to File ---
            # Use index suffix only if more than one eligible table is found on page
            file_index = count + 1 if len(eligible_tables_on_page) > 1 else None
            json_filename = get_clean_filename(article_name, index=file_index)
            file_path = os.path.join(OUTPUT_DIR, json_filename)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(final_output, f, indent=2, ensure_ascii=False)
                
            print(f"✅ Success! Table #{original_index+1} saved as {json_filename} ({len(records)}x{len(df.columns)}).")
        
        print(f"✨ Finished page: Found {len(eligible_tables_on_page)} eligible tables.")

    except Exception as e:
        print(f"🚨 Error: {e}")
        if not is_random: break
        time.sleep(1)

if not found_any_eligible_page and is_random:
    print("\n🏁 Finished processing the list. No table met the criteria.")