import os
import requests
import csv
from .models import WEBSITES

def DownloadCarData(url, output_path):
    #if os.path.exists(output_path):
    #    os.remove(output_path)

    # Download the csv through hosted source #
    #response = requests.get(url)
    #response.raise_for_status()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    #with open(output_path, 'w', newline='', encoding='utf-8') as csv_file:
    #    csv_file.write(response.text)

# Create each one of the website data csvs
DATA_FIELDS = ['make', 'model', 'year', 'price', 'kilometers', 'link']

for website_name, tbl in WEBSITES.items():
    output_path = f"./scraper/data/{website_name}.csv"
    if os.path.exists(output_path):
        os.remove(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames = DATA_FIELDS)
        writer.writeheader()
##

def WriteRowToSiteCSV(website_name, row):
    output_path = f"./scraper/data/{website_name}.csv"
    complete_row = {header: row.get(header, None) for header in DATA_FIELDS}
    with open(output_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames = DATA_FIELDS)
        writer.writerow(complete_row)