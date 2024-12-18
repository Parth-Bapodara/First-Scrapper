import scrapy
from ..items import FirstProjectItem,AnsweredByInfo
import logging

logger = logging.getLogger(__name__)

class StackOverSpider(scrapy.Spider):
    name = "stack"
    allowed_domains = ["stackoverflow.com"]
    start_urls = ['https://stackoverflow.com/questions?tab=Active']

    def parse(self, response):
        for question in response.css("div.s-post-summary"):
            question_link = response.urljoin(question.css("h3 a::attr(href)").get())
            yield response.follow(question_link, callback=self.parse_question)

    def parse_question(self, response):
        answers = response.css("div.answer")
        if answers: 
            item = FirstProjectItem()

            item["title"] = response.css("h1 a::text").get()
            item["link"]  = response.url
            item["tags"]  = response.css("div.post-taglist a::text").getall()

            question_author = response.css("div.post-layout--right div.user-info")
            item["asked_by"] = {
                "name": question_author.css("div.user-details a::text").get(),
                "asked-time": response.css("time::attr(datetime)").get(),
                "reputation": question_author.css("div.-flair span.reputation-score::text").get(),
                "gold"  : question_author.css("span.badge1 + span::text").get(default="0"),
                "silver": question_author.css("span.badge2 + span::text").get(default="0"),
                "bronze": question_author.css("span.badge3 + span::text").get(default="0"),
            }
            
            accepted_answer = response.css("div.answer.accepted-answer div.s-prose p::text").getall()
            item["accepted_answer"] = " ".join(accepted_answer).strip() if accepted_answer else None
            
            accepted_answer_demo = response.css("div.answer.accepted-answer div.user-info")
            if item["accepted_answer"]:
                item["answered_by"] = {
                "name": accepted_answer_demo.css("div.user-details a::text").get(),
                "answered-time": accepted_answer_demo.css("div.d-flex span.relativetime::text").get(),
                "reputation": accepted_answer_demo.css("div.-flair span.reputation-score::text").get(),
                "gold"  : accepted_answer_demo.css("span.badge1 + span::text").get(default="0"),
                "silver": accepted_answer_demo.css("span.badge2 + span::text").get(default="0"),
                "bronze": accepted_answer_demo.css("span.badge3 + span::text").get(default="0"),
            }

            other_answers = []
            for answer in response.css("div.answer"):
                answer_text = answer.css("div.s-prose p::text").getall()
                if answer_text:
                    other_answers.append(" ".join(answer_text).strip())

            item["other_answers"] = other_answers
            if item["other_answers"]:
                user_details=[]
                for answer in item["other_answers"]:
                    answer = response.css("div.answer div.s-prose::text").getall()
                    answer_demo = answer
                    answered_by_other = {
                        "name": answer_demo.css("div.user-details a::text").get(),
                        "answered-time": answer_demo.css("div.d-flex span.relativetime::text").get(),
                        "reputation": answer_demo.css("div.-flair span.reputation-score::text").get(),
                        "gold"  : answer_demo.css("span.badge1 + span::text").get(default="0"),
                        "silver": answer_demo.css("span.badge2 + span::text").get(default="0"),
                        "bronze": answer_demo.css("span.badge3 + span::text").get(default="0"),
                    }
                    user_details.append(answered_by_other)

                item["answered_by_other"] = user_details

            # answer_text_demo = response.css("div.answer div.sprose p::text").getall()
            # if item["other_answers"]:
            #     item["answered_by_other"] = {
            #     "name": answer_text_demo.css("div.user-details a::text").get(),
            #     "asked-time": response.css("time::attr(datetime)").get(),
            #     "reputation": answer_text_demo.css("div.-flair span.reputation-score::text").get(),
            #     "gold"  : answer_text_demo.css("span.badge1 + span::text").get(default="0"),
            #     "silver": answer_text_demo.css("span.badge2 + span::text").get(default="0"),
            #     "bronze": answer_text_demo.css("span.badge3 + span::text").get(default="0"),
            # }
            
            yield item

            
