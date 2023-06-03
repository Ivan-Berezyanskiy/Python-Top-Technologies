import scrapy
from scrapy.http import Response

from djinni_scrapy.items import DjinniScrapyItem


class TechnologiesSpider(scrapy.Spider):
    name = "technologies"
    allowed_domains = ["djinni.co"]
    base_url = "https://djinni.co"
    start_urls = ["https://djinni.co/jobs/?primary_keyword=Python"]

    def parse(self, response: Response, **kwargs):
        vacancies = response.css("a.profile::attr(href)").getall()

        for relative_url in vacancies:
            yield response.follow(self.base_url + relative_url,
                                  self.parse_detail_page)
        next_page_url = response.css(
            "li:last-child > a.page-link::attr(href)"
        ).get()

        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)

    @staticmethod
    def parse_detail_page(response: Response):
        experience = int(response.css(
            ".job-additional-info--item:last-child > div::text"
        ).get().strip().split()[0])

        applications = int(response.css("p.text-muted").re(r"(\d+) відгук")[0])

        views = int(response.css("p.text-muted").re(r"(\d+) перегляд")[0])

        tags = response.css(
            ".job-additional-info--item:nth-child(2) > div > span::text"
        ).getall()

        salary = response.css(".detail--title-wrapper span::text").get()

        if experience == "Без":
            experience = 0
        else:
            experience = int(experience)

        if salary:
            min_salary, max_salary = map(
                int, salary.replace("$", "").split("-")
            )
        else:
            min_salary = None
            max_salary = None

        yield DjinniScrapyItem(
            tags=tags,
            experience=experience,
            min_salary=min_salary,
            max_salary=max_salary,
            views=views,
            applications=applications
        )
