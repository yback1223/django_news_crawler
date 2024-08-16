import requests
import logging, time
from collections import deque
from datetime import datetime
from typing import Optional
from bs4 import BeautifulSoup
from .models import Us, World, Politics, Business
from .gemini_work import GeminiWork
from dateutil import parser
from dateutil.tz import gettz

logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s - %(levelname)s - %(message)s",
	handlers=[
		logging.FileHandler("news_crawler.log"),
		logging.StreamHandler()
	]
)

class NewsCrawler:
	def __init__(self):
		self.news_dict = {
			'US': ['https://edition.cnn.com/us', Us, deque(maxlen=10)],
			'World': ['https://edition.cnn.com/world', World, deque(maxlen=10)],
			'Politics': ['https://edition.cnn.com/politics', Politics, deque(maxlen=10)],
			'Business': ['https://edition.cnn.com/business', Business, deque(maxlen=10)],
		}

	def crawl_news(self):
		for key, value in self.news_dict.items():
			url = value[0]
			model = value[1]
			links = value[2]
			try:
				response = requests.get(url)
				response.raise_for_status()
				soup = BeautifulSoup(response.content, 'html.parser')
				first_news_section = soup.find('div', class_='container__field-links container_lead-plus-headlines__field-links')

				if first_news_section:
					for one_news in first_news_section.find_all('a', class_='container__link container__link--type-article container_lead-plus-headlines__link'):
						time.sleep(10)
						link = one_news['href']
						if link not in links:
							links.append(link)
							full_link = f"https://edition.cnn.com{link}"
							article = self.get_article(full_link)
							if article:
								self.save_article(article, full_link, model)
							else:
								logging.warning(f"Failed to retrieve article from {full_link}")
			except requests.exceptions.RequestException as e:
				logging.error(f"Failed to crawl {url}: {e}", exc_info=True)
			except Exception as e:
				logging.error(f"An unexpected error occurred while processing {url}: {e}", exc_info=True)

	def save_article(self, article, full_link, model):
		try:
			model.objects.create(
				title=article['headline'],
				content=article['content'],
				url_link=full_link,
				published_date=article['published_date'],
			)
			logging.info(f"Article saved: {article['headline']}")
		except Exception as e:
			logging.error(f"Failed to save article {article['headline']}: {e}", exc_info=True)

	def get_article(self, link):
		try:
			response = requests.get(link)
			response.raise_for_status()
			soup = BeautifulSoup(response.content, 'html.parser')
			headline = self.get_headline(soup)
			content = self.get_content(soup)
			published_date = self.get_published_time(soup)
			print(f'published_date = {published_date}')
			cooked_contents = GeminiWork().summarize_content(headline, content)
			return {
				'link': link,
				'headline': cooked_contents['translated_headline'],
				'content': cooked_contents['summarized_content'],
				'published_date': published_date
			}
		except requests.exceptions.RequestException as e:
			logging.error(f"Failed to retrieve article {link}: {e}", exc_info=True)
		except Exception as e:
			logging.error(f"An unexpected error occurred while retrieving article {link}: {e}", exc_info=True)
		return None

	def get_headline(self, soup) -> Optional[str]:
		try:
			headline_h1 = soup.find('h1', class_='headline__text inline-placeholder vossi-headline-primary-core-light')
			if headline_h1:
				return headline_h1.get_text(strip=True)
		except Exception as e:
			logging.error(f"Failed to get headline: {e}", exc_info=True)
		return None

	def get_published_time(self, soup) -> Optional[datetime]:
		try:
			byline_div = soup.find('div', class_='headline__byline-sub-text')
			if byline_div:
				timestamp_div = byline_div.find('div', class_='timestamp vossi-timestamp-primary-core-light')
				if timestamp_div:
					lines = [line.strip() for line in timestamp_div.get_text().splitlines() if line.strip()]
					tzinfos = {
						'EDT': gettz('America/New_York'),  # Eastern Daylight Time (미국 동부 시간대)
						'EST': gettz('America/New_York'),  # Eastern Standard Time (미국 동부 표준시)
					}
					timestamp_text = ' '.join(lines[1:]).strip()
					
					published_datetime = parser.parse(timestamp_text, tzinfos=tzinfos)
					return published_datetime
		except ValueError as e:
			logging.error(f"Failed to parse published time: {e}", exc_info=True)
		except Exception as e:
			logging.error(f"Failed to get published time: {e}", exc_info=True)
		return None
	
	def get_content(self, soup) -> Optional[str]:
		try:
			paragraphs = soup.find_all('p', class_='paragraph inline-placeholder vossi-paragraph-primary-core-light')
			if paragraphs:
				return ' '.join([p.get_text(strip=True) for p in paragraphs])
		except Exception as e:
			logging.error(f"Failed to get content: {e}", exc_info=True)
		return None
