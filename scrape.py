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
url = "https://en.wikipedia.org/wiki/Special:Random"
headers = {'User-Agent': 'Mozilla/5.0'}

# Define thresholds
MIN_ROWS = 10
MIN_COLS = 4

valid_table_found = False
attempts = 0

print(f"🚀 Starting scraper. Searching for a table with at least {MIN_ROWS} rows and {MIN_COLS} columns...")

while not valid_table_found:
    attempts += 1
    print(f"\n--- Attempt #{attempts} ---")
    
    # --- 3. Fetch ---
    try:
        response = requests.get(url, headers=headers, timeout=10)
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
            continue

        table_stats = []
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

                # --- 5. Column Analysis (Quantitative vs Qualitative) ---
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
                        "attempts_made": attempts
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
                break 
        
        if not valid_table_found:
            print(f"⚠️ Tables found but too small: {', '.join(table_stats)}")
            # Short sleep to be polite to Wikipedia servers
            time.sleep(0.5)

    except Exception as e:
        print(f"🚨 Network or parsing error: {e}")
        time.sleep(2)