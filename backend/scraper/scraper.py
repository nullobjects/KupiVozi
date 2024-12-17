#Scrapy	Large-scale scraping with high efficiency	- Asynchronous, fast
#- Built-in crawling
#- Scalable and production-ready

# Vehicle data used from
# https://public.opendatasoft.com/explore/dataset/all-vehicles-model/api/

import scrapy
from .models import WEBSITES
from .data_download import WriteRowToSiteCSV
from .data_preprocess import ExtractCarInfo

class Reklama5Spider(scrapy.Spider):
    name = "reklama5"
    allowed_domains = [WEBSITES["reklama5"]["domain"]]
    start_urls = [WEBSITES["reklama5"]["listings"]]

    def parse(self, response):
        for car in response.css(".ad-desc-div.col-lg-6.text-left"):
            title = car.css("h3 a::text").get().strip()
            tags = " ".join(
                text.strip() for text in car.css("p::text").getall() if text.strip() and text.strip() != "•"
            )
            description = car.css(".searchAdDesc::text").get().strip()
            price = car.css(".search-ad-price::text").get().strip()

            full_text = title + " " + tags + " " + description + " " + price
            print(ExtractCarInfo(full_text))
            #print("--------------")
            #print(title)
            #print(tags)
            #print(description)
            #print(price)
            #print("-----------")
            #WriteRowToSiteCSV({
            #    'name': car.css('h3 a::text').get(),
            #    'price': car.css('p').get(),
            #    'link': response.urljoin(car.css('a::attr(href)').get()),
            #})

        pages_str = response.css(".number-of-pages::text").get()
        if pages_str:
            pages_str = pages_str.split()
            page_number = int(pages_str[1])
            total_pages = int(pages_str[3])

            #if page_number < total_pages:
            #    #next_page = WEBSITES["reklama5"]["listings"][:-1] + str(page_number + 1)
            #    #yield scrapy.Request(next_page, callback=self.parse)
            #else:
            #    self.log("Done scraping reklama5!")