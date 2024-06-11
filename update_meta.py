import pandas as pd
from bs4 import BeautifulSoup
import os
import time
from colorama import init, Fore, Style
import urllib.parse

# Initialize colorama
init(autoreset=True)

# Correct the file path and ensure it has the .csv extension
csv_file = r'C:\Users\DAILY USE\Downloads\applesteel-meta-title.csv'
html_directory = r'C:\Users\DAILY USE\Downloads\applesteel-meta'

# Load CSV file and strip column names
try:
    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.strip()  # Strip leading/trailing whitespace from column names
    print(df.columns)  # Print column names for debugging
except FileNotFoundError:
    print(f"{Fore.RED}CSV file not found: {csv_file}")
    exit()

# Function to update meta title in HTML file
def update_meta_title_in_html(html_file, new_title):
    try:
        with open(html_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')

        # Find or create the title tag
        title_tag = soup.find('title')
        if title_tag:
            title_tag.string = new_title
        else:
            head_tag = soup.find('head')
            if head_tag:
                new_title_tag = soup.new_tag('title')
                new_title_tag.string = new_title
                head_tag.append(new_title_tag)

        # Convert BeautifulSoup object back to string without escaping special characters
        html_string = str(soup.prettify(formatter=None))

        # Write the modified content back to the file
        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(html_string)

        print(f"{Fore.GREEN}Updated: {html_file}")

    except FileNotFoundError:
        print(f"{Fore.RED}File not found: {html_file}")
    except Exception as e:
        print(f"{Fore.RED}Error processing file {html_file}: {e}")

# Group title updates by their respective HTML files
updates_by_file = {}
for index, row in df.iterrows():
    page_url = row['URL']
    new_title = row['New Meta Title']

    # Extract path from the URL
    parsed_url = urllib.parse.urlparse(page_url)
    path = parsed_url.path
    if path.endswith('/'):
        path = os.path.join(path, 'index.html')
    filename = path.strip('/')
    html_file_path = os.path.join(html_directory, filename)

    if os.path.exists(html_file_path):
        updates_by_file[html_file_path] = new_title
    else:
        print(f"{Fore.RED}File does not exist: {html_file_path}")

# Update each HTML file with the respective new title
total_files = len(updates_by_file)
start_time = time.time()

for i, (html_file, new_title) in enumerate(updates_by_file.items()):
    update_meta_title_in_html(html_file, new_title)

    # Print progress
    elapsed_time = time.time() - start_time
    print(f"Processed {i + 1}/{total_files} HTML files. Elapsed time: {elapsed_time:.2f} seconds.")

print(f"{Fore.GREEN}Meta titles updated successfully.")
