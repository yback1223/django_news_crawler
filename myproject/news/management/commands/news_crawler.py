from django.core.management.base import BaseCommand
from news.news_crawler import NewsCrawler

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        crawler = NewsCrawler()
        crawler.crawl_news()
        self.stdout.write(self.style.SUCCESS('Successfully crawled news articles'))
