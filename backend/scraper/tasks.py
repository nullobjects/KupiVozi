from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .scraper import Reklama5Spider
from .data_download import DownloadCarData
from .data_preprocess import PreProcessPartsDataForTraining
from .nlp_models import DamagedOrForPartsModel
from sklearn.metrics import accuracy_score
import os
import logging

# Get rid of tensorflow logs and messages #
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Django likes to run stuff twice
if os.environ.get('RUN_MAIN') == 'true':
    # Data pipeline is here #

    # Scraper fetches all data #
    def start_scraper():
        process = CrawlerProcess(get_project_settings())
        process.crawl(Reklama5Spider)
        process.start()

    start_scraper()

    # Download car data (makes, models, years ...)
    CAR_DATA_URL = "NO HOSTED URL AS OF NOW"
    DownloadCarData(CAR_DATA_URL, "./scraper/data/car_data.csv")

    # Data is preprocessed for training #
    train_dataset, test_x, test_y = PreProcessPartsDataForTraining()

    model = DamagedOrForPartsModel()

    model.fit(train_dataset, epochs=15, batch_size=32)
    predictions = model.predict(test_x)
    predictions = (predictions > 0.5).astype(int).flatten()

    accuracy = accuracy_score(test_y, predictions)
    print(f"Accuracy score of parts model: {accuracy:.4f}")