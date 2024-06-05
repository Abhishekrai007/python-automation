import pandas as pd
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin

# Correct the file path and ensure it has the .csv extension
csv_file = r'C:\Users\DAILY USE\Desktop\bhansalioversease-alt.csv'
html_directory = r'C:\Users\DAILY USE\Downloads\bhansalioversease'

try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    print(f"CSV file not found: {csv_file}")
    exit()

# Function to update alt text in HTML file
def update_alt_text_in_html(html_file, image_url, alt_text):
    try:
        with open(html_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        # Find all img tags
        img_tags = soup.find_all('img')
        for img in img_tags:
            # Convert relative image URLs to absolute
            img_src = img.get('src')
            abs_image_url = urljoin('https://www.bhansalioverseas.com/', img_src)
            if abs_image_url == image_url:
                img['alt'] = alt_text

        # Save the modified HTML back to the file
        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(str(soup))
    except Exception as e:
        print(f"Error processing file {html_file}: {e}")

# Group image updates by their respective HTML files
image_updates_by_file = {}
for index, row in df.iterrows():
    page_url = row['From']
    image_url = row['To']
    alt_text = row['Alt Attribute']
    
    filename = os.path.basename(page_url)
    html_file_path = os.path.join(html_directory, filename)
    
    if html_file_path not in image_updates_by_file:
        image_updates_by_file[html_file_path] = []
    image_updates_by_file[html_file_path].append((image_url, alt_text))

# Update each HTML file with the respective image updates
total_files = len(image_updates_by_file)
start_time = time.time()

for i, (html_file, updates) in enumerate(image_updates_by_file.items()):
    for image_url, alt_text in updates:
        update_alt_text_in_html(html_file, image_url, alt_text)
    
    # Print progress
    elapsed_time = time.time() - start_time
    print(f"Processed {i + 1}/{total_files} HTML files. Elapsed time: {elapsed_time:.2f} seconds.")

print("Alt text updated successfully.")
