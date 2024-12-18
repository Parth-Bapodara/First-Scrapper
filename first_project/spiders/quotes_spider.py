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


# def parse_question(self, response):
#     answers = response.css("div.answer")
#     if answers: # Only process if answers exist
#         item = FirstProjectItem()

#         # Question details
#         item["title"] = response.css("h1 a::text").get()
#         item["link"] = response.url
#         item["tags"] = response.css("div.post-taglist a::text").getall()

#         # Question author (asked by)
#         question_author = response.css("div.post-layout--right div.user-info")
#         item["asked_by"] = {
#             "name": question_author.css("div.user-details a::text").get(),
#             "reputation": question_author.css("span.reputation-score::text").get(default="0").replace(",", ""),
#             "gold_badges": question_author.css("span.badge1 + span::text").get(default="0"),
#             "silver_badges": question_author.css("span.badge2 + span::text").get(default="0"),
#             "bronze_badges": question_author.css("span.badge3 + span::text").get(default="0"),
#             "asked_time": response.css("time::attr(datetime)").get(),
#         }

#         # Accepted answer
#         accepted_answer = response.css("div.answer.accepted")
#         accepted_answer_content = accepted_answer.css("div.s-prose p::text").getall()
#         item["accepted_answer"] = " ".join(accepted_answer_content).strip() if accepted_answer_content else None

#         # Extract all answer details
#         answer_details = []
#         for answer in answers:
#             user_info = answer.css("div.user-info")
#             answer_detail = {
#                 "name": user_info.css("div.user-details a::text").get(),
#                 "answered_time": answer.css("time::attr(datetime)").get(),
#                 "reputation": user_info.css("span.reputation-score::text").get(default="0").replace(",", ""),
#                 "gold_badges": user_info.css("span.badge1 + span::text").get(default="0"),
#                 "silver_badges": user_info.css("span.badge2 + span::text").get(default="0"),
#                 "bronze_badges": user_info.css("span.badge3 + span::text").get(default="0"),
#                 "content": " ".join(answer.css("div.s-prose p::text").getall()).strip(),
#                 "is_accepted": bool(answer.css("div.accepted")), # True if this is the accepted answer
#             }
#             answer_details.append(answer_detail)

#         item["answer_details"] = answer_details
#         yield item

