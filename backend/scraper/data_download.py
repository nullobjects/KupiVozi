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

    for index, tbl in WEBSITES.items():
        output_path = f"./scraper/data/{index}.csv"
        file_exists = os.path.isfile(output_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        with open(output_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Make", "Model", "Description", "Condition"])
            if not file_exists:
                writer.writeheader()

def WriteRowToSiteCSV(website_name, row):
    output_file = f"./scraper/data/{website_name}.csv"
    file_exists = os.path.isfile(output_file)
    if file_exists:
        with open(output_file, mode='a', newline='', encoding='utf-8') as file:
            file.write(row)