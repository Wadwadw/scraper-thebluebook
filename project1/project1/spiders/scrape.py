import scrapy
import random
from scrapy import Selector
from selenium.webdriver.support.ui import WebDriverWait
from capmonster_python import NoCaptchaTaskProxyless
from scrapy_selenium import SeleniumRequest


class V3Spider(scrapy.Spider):
    name = "scrape"
    allowed_domains = ["www.thebluebook.com"]
    website_key = "6LcVPAcUAAAAAFfXArD3YoSWjJbmcc0a38J6fM6A"
    captcha = NoCaptchaTaskProxyless(client_key="###########")

    def __init__(self):
        super().__init__()
        self.user_list = []
        with open(
            r"C:\Games\trainee\pr1\project1\project1\spiders\user.txt", "r"
        ) as file:
            for line in file:
                self.user_list.append(line)

    page = 0

    def start_requests(self):
        rand = random.choice(self.user_list)
        yield SeleniumRequest(
            url="https://www.thebluebook.com/search.html?region=16&class=0060",
            callback=self.parse,
            headers={"User-Agent": rand},
        )
        self.user_list.remove(rand)

    def parse(self, response):
        driver = response.meta["driver"]
        self.page += 1
        rand = random.choice(self.user_list)
        url = driver.current_url
        self.html = driver.page_source
        if "Captcha" in driver.title:
            taskId = self.captcha.createTask(url, self.website_key)
            resp = self.captcha.joinTaskResult(taskId)
            driver.execute_script(
                f"document.getElementsByClassName('g-recaptcha-response')[0].innerHTML = '{resp}';"
            )
            WebDriverWait(driver, 3).until(
                lambda d: d.find_element_by_xpath(
                    "//div[contains(@class,'single_result_wrapper')]/div[@class='media']/div[contains(@class,'media-body')]"
                )
            )

            self.html = driver.page_source
        respons = Selector(text=self.html)
        normales = respons.xpath(
            "//div[contains(@class,'single_result_wrapper')]/div[@class='media']/div[contains(@class,'media-body')]"
        )
        for normal in normales:
            yield {
                "Company-name": normal.xpath(".//h3/a/span/text()").get(),
                "City": normal.xpath(
                    ".//div[@class='addy_wrapper']/span/span[@itemprop='addressLocality']/text()"
                ).get(),
                "State": normal.xpath(
                    ".//div[@class='addy_wrapper']/span/span[@itemprop='addressRegion']/text()"
                ).get(),
                "Zip-code": normal.xpath(
                    ".//div[@class='addy_wrapper']/span/span[@itemprop='postalCode']/text()"
                ).get(),
                "Phone-number": normal.xpath(
                    ".//span[@itemprop='telephone']/text()"
                ).get(),
                "Website": normal.xpath(
                    ".//a[@class='website-link external-trigger']/@href"
                ).get(),
                "Page": self.page,
            }

        next_page = respons.xpath(
            "(//div[@class='pager-outer-wrapper']/div)[last()]/a/@href"
        ).get()
        if next_page:
            absolute_url = f"https://www.thebluebook.com/{next_page}"
            yield SeleniumRequest(
                url=absolute_url,
                wait_time=3,
                callback=self.parse,
                headers={"User-Agent": rand},
            )
        self.user_list.remove(rand)
