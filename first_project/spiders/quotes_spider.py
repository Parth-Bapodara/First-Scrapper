import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
    ]

    # def start_requests(self):
    #     urls = [
    #         "https://quotes.toscrape.com/page/1/",
    #         "https://quotes.toscrape.com/page/2/",
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("span small::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            # next_page = response.urljoin(next_page)
            yield response.follow(next_page, callback=self.parse)
    
    # def parse(self, response):
    #     for quote in response.css("div.quote"):
    #         yield {
    #             "text": quote.css("span.text::text").get(),
    #             "author": quote.css("small.author::text").get(),
    #             "tags": quote.css("div.tags a.tag::text").getall(),
    #         }
        # page = response.url.split("/")[-2]
        # filename = f"quotes-{page}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")





# stats = response.css("div.s-post-summary--stats-item")
# votes = views = "0"

# for stat in stats:
#     label = stat.css("span::text").get(default="").strip().lower()
#     if "vote" in label: # Check if the label mentions votes
#         votes = stat.css("div.s-post-summary--stats-item-number::text").get(default="0").strip()
#     elif "view" in label: # Check if the label mentions views
#         views = stat.css("div.s-post-summary--stats-item-number::text").get(default="0").strip()

# item["votes"] = votes
# item["views"] = views


# import scrapy
# from ..items import FirstProjectItem

# class StackOverSpider(scrapy.Spider):
#     name = "stack"
#     allowed_domains = ["stackoverflow.com"]
#     start_urls = ['https://stackoverflow.com/questions?tab=Active']

#     def parse(self, response):
#         for question in response.css("div.s-post-summary"):
#             question_link = response.urljoin(question.css("h3 a::attr(href)").get())
#             yield response.follow(question_link, callback=self.parse_question)

# #     mport scrapy
# from ..items import FirstProjectItem

# class StackOverSpider(scrapy.Spider):
#     name = "stack"
#     allowed_domains = ["stackoverflow.com"]
#     start_urls = ['https://stackoverflow.com/questions?tab=Active']

#     def parse(self, response):
#         for question in response.css("div.s-post-summary"):
#             question_link = response.urljoin(question.css("h3 a::attr(href)").get())
#             yield response.follow(question_link, callback=self.parse_question)

#     def parse_question(self, response):
#         # Initialize the item
#         item = FirstProjectItem()

#         # Extracting votes and views using a loop
#         stats = response.css("div.s-post-summary--stats div.s-post-summary--stats-item")
#         votes, views = None, None

#         for stat in stats:
#             label = stat.css("span::attr(title)").get() # Example: "votes", "views"
#             value = stat.css("span.s-post-summary--stats-item-number::text").extract_first(default="0").strip()
#             if "vote" in label.lower():
#                 votes = value
#             elif "view" in label.lower():
#                 views = value

#         # Storing in the item
#         item["votes"] = votes or "0" # Default to "0" if not found
#         item["views"] = views or "0"

#         # Extracting question details
#         item["title"] = response.css("h1 a::text").get()
#         item["link"] = response.url
#         item["tags"] = response.css("div.post-taglist a::text").getall()
