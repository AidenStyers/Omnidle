import pandas as pd
import requests
import os
import re
import json
import time
from io import StringIO
from bs4 import BeautifulSoup

# --- 1. Helper Function ---
def to_camel_case(text):
    # Remove non-alphanumeric characters and split by whitespace
    words = re.sub(r'[^a-zA-Z0-9\s]', '', text).split()
    if not words:
        return "scrapedData.js"
    # lowercase first word, capitalize subsequent words
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:]) + ".js"

# --- 2. Setup ---
random_url = "https://en.wikipedia.org/wiki/Special:Random"
headers = {'User-Agent': 'Mozilla/5.0'}

# Define thresholds
MIN_ROWS = 10
MIN_COLS = 4

# --- 3. User Input ---
user_input = input("Enter a Wikipedia URL (or press Enter for a random article): ").strip()
target_url = user_input if user_input else random_url
is_random = not user_input

valid_table_found = False
attempts = 0

if is_random:
    print(f"🚀 Random Mode: Searching for a table with at least {MIN_ROWS} rows and {MIN_COLS} columns...")
else:
    print(f"🎯 Target Mode: Attempting to scrape {target_url}...")

while not valid_table_found:
    attempts += 1
    if is_random:
        print(f"\n--- Attempt #{attempts} ---")
    
    try:
        response = requests.get(target_url, headers=headers, timeout=10)
        final_url = response.url 
        soup = BeautifulSoup(response.text, 'html5lib')

        # Extract article name
        article_name = soup.title.string.replace(" - Wikipedia", "") if soup.title else "Unknown Article"
        print(f"Checking: '{article_name}'")

        # --- 4. Parse & Clean Table ---
        html_data = StringIO(response.text)
        try:
            tables = pd.read_html(html_data, flavor='html5lib')
        except ValueError:
            tables = []

        if not tables:
            print("❌ No tables found in this article.")
            if not is_random: break # Stop if user provided a specific URL
            continue

        table_stats = []
        found_on_this_page = False
        
        for i, df in enumerate(tables):
            rows, cols = df.shape
            table_stats.append(f"T{i+1}: {rows}x{cols}")
            
            if rows >= MIN_ROWS and cols >= MIN_COLS:
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

                # --- 6. Prepare Final Structure ---
                records = df.to_dict(orient='records')

                final_output = {
                    "metadata": {
                        "source_url": final_url,
                        "article_name": article_name,
                        "row_count": len(records),
                        "column_count": len(df.columns),
                        "column_analysis": column_types,
                        "attempts_made": attempts,
                        "mode": "random" if is_random else "target"
                    },
                    "data": records
                }

                # --- 7. Save to File ---
                script_dir = os.path.dirname(os.path.abspath(__file__))
                js_filename = to_camel_case(article_name)
                file_path = os.path.join(script_dir, js_filename)
                
                formatted_json = json.dumps(final_output, indent=2)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"const tableData = {formatted_json};")
                    
                print(f"✅ Success! Found valid table ({rows}x{cols}).")
                print(f"📄 Saved to: {js_filename}")
                print(f"🔗 Source: {final_url}")
                valid_table_found = True
                found_on_this_page = True
                break 
        
        if not found_on_this_page:
            if is_random:
                print(f"⚠️ Tables found but too small: {', '.join(table_stats)}")
                time.sleep(0.5)
            else:
                print(f"❌ The provided URL did not have a table meeting the requirements ({MIN_ROWS}x{MIN_COLS}).")
                print(f"📊 Table sizes found: {', '.join(table_stats)}")
                break # Exit loop for specific URLs

    except Exception as e:
        print(f"🚨 Error: {e}")
        if not is_random: break
        time.sleep(2)