# import sys,os
# sys.path.append(os.path.abspath('......./Config.config'))
from pathlib import Path
import scrapy,os
from ..items import FirstProjectItem
import logging, smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
#from Config.config import settigs

load_dotenv()
logger = logging.getLogger(__name__)

class StackOverSpider(scrapy.Spider):
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
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
            item["total_answers"] = len(answers)

            stats = response.css("div.s-post-summary--stats")

            item["views"] = stats.css("div.s-post-summary--stats-item:nth-child(3) span.s-post-summary--stats-item-number::text").get()
            item["votes"] = stats.css("div.s-post-summary--stats-item:nth-child(1) span.s-post-summary--stats-item-number::text").get()

            # item["views"] = stats.css(".s-post-summary--stats:nth-child(1) .s-post-summary--stats-item-number::text").get()
            # item["votes"] = stats.css(".s-post-sumary--stats:nth-child(3) .s-post-summary--stats-item-number::text").get()

            # demo_details = []

            # for stat in response.css("div.s-post-summary--stats-item"):

            #     label = stat.css("div::attr(title)").get().lower()
            #     value = stat.css("span.s-post-summary--stats-item-number::text").get()
            #     if "score" in label:
            #         votes = value if votes else None
            #     elif "view" in label:
            #         views = value if views else None

            #     demo_det = {
            #         "votes": votes,
            #         "views": views
            #     }
            #     demo_details.append(demo_det)
            
            # item["details"] = demo_details

            question_author = response.css("div.post-layout--right div.user-info")
            item["asked_by"] = {
                "name": question_author.css("div.user-details a::text").get(),
                "user-profile-link": response.urljoin(question_author.css("div.user-details a::attr(href)").get()),
                "asked-time": question_author.css("div.d-flex span.relativetime::text").get(),
                "reputation": question_author.css("div.-flair span.reputation-score::text").get(),
                "gold"  : question_author.css("span.badge1 + span::text").get(default="0"),
                "silver": question_author.css("span.badge2 + span::text").get(default="0"),
                "bronze": question_author.css("span.badge3 + span::text").get(default="0"),
            }
            
            answer_detail = []
            for answer in response.css("div.answer"):
                is_accepted = bool(answer.css("div.accepted-answer"))

                answer_parts = answer.css("div.s-prose p::text, div.s-prose pre::text, div.s-prose code::text").getall()
                answer_content = "\n".join([part.strip() for part in answer_parts if part.strip()])

                user_info = answer.css("div.user-info")
                answer_details = {
                    "content": answer_content,
                    "is_accepted": is_accepted,
                    "answered_by":{
                            "name": user_info.css("div.user-details a::text").get(),
                            "user-profile-link": response.urljoin(user_info.css("div.user-details a::attr(href)").get()),
                            "answered_time": user_info.css("div.d-flex span.relativetime::text").get(),
                            "reputation": user_info.css("div.-flair span.reputation-score::text").get(),
                            "gold": user_info.css("span.badge1 + span::text").get(default="0"),
                            "silver": user_info.css("span.badge2 + span::text").get(default="0"),
                            "bronze": user_info.css("span.badge3 + span::text").get(default="0"),

                    }
                }
                answer_detail.append(answer_details)

                if is_accepted in answer_detail:
                    answer_detail = answer_detail.sort()

            item["answer"] = answer_detail

            yield item

    def send_mail():

        msg = EmailMessage()
        msg['From'] = os.getenv("MAIL_FROM")
        msg['To'] = "parth.bapodara@mindinventory.com"
        msg["Subject"] = "Scrapper Output File"
        msg.set_content("Your Requested Output file for Stackoverflow using Scrapy.")
        with open("stack_demo.json", 'r') as f:
            data = f.read()
        msg.add_attachment(data,filename = "stack_demo.json")
        #msg.set_content()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.ehlo()
        server.login(os.getenv("MAIL_FROM"), os.getenv("MAIL_PASSWORD"))
        server.send_message(msg)
        server.quit()

    #send_mail()



# process = CrawlerProcess()
# process.crawl(StackOverSpider)
# process.start()

            # accepted_answer = response.css("div.answer.accepted-answer div.s-prose p::text").getall()
            # item["accepted_answer"] = " ".join(accepted_answer).strip() if accepted_answer else None
            
            # accepted_answer_demo = response.css("div.answer.accepted-answer div.user-info")
            # if item["accepted_answer"]:
            #     item["answered_by"] = {
            #     "name": accepted_answer_demo.css("div.user-details a::text").get(),
            #     "answered-time": accepted_answer_demo.css("div.d-flex span.relativetime::text").get(),
            #     "reputation": accepted_answer_demo.css("div.-flair span.reputation-score::text").get(),
            #     "gold"  : accepted_answer_demo.css("span.badge1 + span::text").get(default="0"),
            #     "silver": accepted_answer_demo.css("span.badge2 + span::text").get(default="0"),
            #     "bronze": accepted_answer_demo.css("span.badge3 + span::text").get(default="0"),
            # }

            # other_answers = []
            # for answer in response.css("div.answer"):
            #     answer_text = answer.css("div.s-prose p::text").getall()
            #     if answer_text:
            #         other_answers.append(" ".join(answer_text).strip())

            # item["other_answers"] = other_answers
            # if item["other_answers"]:
            #     user_details=[]
            #     for answer in item["other_answers"]:
            #         answer = response.css("div.answer div.s-prose::text").getall()
            #         answer_demo = answer
            #         answered_by_other = {
            #             "name": answer_demo.css("div.user-details a::text").get(),
            #             "answered-time": answer_demo.css("div.d-flex span.relativetime::text").get(),
            #             "reputation": answer_demo.css("div.-flair span.reputation-score::text").get(),
            #             "gold"  : answer_demo.css("span.badge1 + span::text").get(default="0"),
            #             "silver": answer_demo.css("span.badge2 + span::text").get(default="0"),
            #             "bronze": answer_demo.css("span.badge3 + span::text").get(default="0"),
            #         }
            #         user_details.append(answered_by_other)

            #     item["answered_by_other"] = user_details

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
            
            

            
