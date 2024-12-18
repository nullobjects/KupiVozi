import scrapy
from ..models import WEBSITES
from ..data_download import WriteRowToSiteCSV
from ..data_preprocess import ExtractCarInfo, IsCarValid

class Pazar3Spider(scrapy.Spider):
    name = "pazar3"
    allowed_domains = [WEBSITES["pazar3"]["domain"]]
    start_urls = [WEBSITES["pazar3"]["listings"]]

    def parse(self, response):
        for car in response.css(".goodssearch-item-content"):
            full_text = ""

            title = car.css(".Link_vis::text").get()
            link = car.css(".Link_vis::attr(href)").get()
            price = car.css(".list-price::text").get()

            full_text = full_text + f" {title} {price}"
            for text in car.css("b::text").getall():
                full_text = full_text + " " + text.strip()

            CarData = ExtractCarInfo(full_text)
            CarData["link"] = WEBSITES["pazar3"]["domain"] + link

            if IsCarValid(CarData):
                WriteRowToSiteCSV("pazar3", CarData)