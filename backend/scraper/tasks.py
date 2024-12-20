from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings
from .data_download import DownloadCarData
from .data_preprocess import PreProcessPartsDataForTraining
from .nlp_models import DamagedOrForPartsModel
from .spiders import Pazar3Spider, Reklama5Spider, VoziSpider
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import load_model
import os
import logging

CAR_DATA_URL = "NO HOSTED URL AS OF NOW"

# Get rid of tensorflow logs and messages #
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Django likes to run stuff twice
if os.environ.get('RUN_MAIN') == 'true':
    # Data pipeline is here #

    # Scraper runs asynchronously and gets the data from all websites #
    def start_scraper():
        runner = CrawlerRunner(get_project_settings())

        spiders = [Pazar3Spider, Reklama5Spider]#, VoziSpider]

        @defer.inlineCallbacks
        def crawl():
            for spider in spiders:
                yield runner.crawl(spider)
            reactor.stop()
        crawl()
        reactor.run()
    start_scraper()

    # Download car data (makes, models, years ...)
    DownloadCarData(CAR_DATA_URL, "./scraper/data/car_data.csv")

    # Data is preprocessed for training #
    train_dataset, test_x, test_y = PreProcessPartsDataForTraining()

    model_path = "./scraper/data/models/parts_model.h5"

    if os.path.exists(model_path):
        print("Loading saved model...")
        model = load_model(model_path)
    else:
        print("No saved model found. Training a new model...")
        model = DamagedOrForPartsModel()
        model.fit(train_dataset, epochs=15, batch_size=32)
        model.save(model_path)  # Save the model for future use
        print(f"Model saved to {model_path}")

    predictions = model.predict(test_x)
    predictions = (predictions > 0.5).astype(int).flatten()

    accuracy = accuracy_score(test_y, predictions)
    print(f"Accuracy score of parts model: {accuracy:.4f}")