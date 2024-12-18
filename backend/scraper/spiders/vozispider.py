import scrapy
from ..models import WEBSITES
from ..data_download import WriteRowToSiteCSV
from ..data_preprocess import ExtractCarInfo, IsCarValid

# Needs work #
class VoziSpider(scrapy.Spider):
    name = "vozi"
    allowed_domains = [WEBSITES["vozi"]["domain"]]
    start_urls = [WEBSITES["vozi"]["listings"]]

    def parse(self, response):
        for car in response.css(".listing-box__info-wrap"):
            title = car.css("listing-box__title::text").get().strip()
            link = car.css("h3 a").attrib["href"]
            tags = " ".join(
                text.strip() for text in car.css("p::text").getall() if text.strip() and text.strip() != "•"
            )
            description = car.css(".searchAdDesc::text").get().strip()
            price = car.css(".listing-box__price::text").getall().strip()
            print(price)

            full_text = title + " " + tags + " " + description + " " + price

            CarData = ExtractCarInfo(full_text)
            CarData["link"] = WEBSITES["vozi"]["domain"] + link
            
            if IsCarValid(CarData):
                WriteRowToSiteCSV("vozi", CarData)

        pages_str = response.css(".number-of-pages::text").get()
        if pages_str:
            pages_str = pages_str.split()
            page_number = int(pages_str[1])
            total_pages = int(pages_str[3])

            #if page_number < total_pages:
            #    #next_page = WEBSITES["vozi"]["listings"][:-1] + str(page_number + 1)
            #    #yield scrapy.Request(next_page, callback=self.parse)
            #else:
            #    self.log("Done scraping vozi!")

