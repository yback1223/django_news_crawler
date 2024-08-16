import time
import google
import google.generativeai as genai
import logging
import re

from decouple import config

logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s - %(levelname)s - %(message)s",
	handlers=[
		logging.FileHandler("gemini_work.log"),
		logging.StreamHandler()
	]
)

class GeminiWork:
	def __init__(self):
		self.api_key = config('GEMINI_API_KEY')

	def summarize_content(self, headline, content, retries=3):

		prompt = f"""
			I will provide you with a headline and an article. 
			Please translate the headline into Korean appropriately. 
			For the article, summarize it in Korean in 200 characters. 
			Return the result in the following format:
			translated_headline_response || summarized_content_response
			Here is the headline: {headline}
			And here is the article: {content}
			"""

		try:
			generation_config = {
				"temperature": 1,
				"top_p": 0.95,
				"top_k": 64,
				"max_output_tokens": 1024,  # 줄어든 token 제한
				"response_mime_type": "text/plain",
			}

			genai.configure(api_key=self.api_key)
			model = genai.GenerativeModel(
				model_name="gemini-1.5-flash",
				generation_config=generation_config,
			)

			chat_session = model.start_chat(history=[])

			for attempt in range(retries):
				try:
					logging.info(f"Attempt {attempt + 1} to generate content.")
					response = chat_session.send_message(prompt)

					if response and hasattr(response, 'text'):
						if hasattr(response, 'finish_reason') and response.finish_reason in ["SAFETY"]:
							logging.warning("Response finished due to safety concerns. Retrying...")
							continue

					cleaned_text = re.sub(r'^```json|```$', '', response.text.strip(), flags=re.MULTILINE)
					result_text = cleaned_text.split("||")
					if len(result_text) == 2:
						return {
							'translated_headline': result_text[0].strip(),
							'summarized_content': result_text[1].strip()
						}
					else:
						logging.error(f"Unexpected format in the response: {cleaned_text}")
						continue

				except google.generativeai.types.generation_types.StopCandidateException as e:
					logging.error(f"Safety settings triggered on attempt {attempt + 1}: {e}", exc_info=True)
					break
				except Exception as e:
					logging.error(f"Error during generation attempt {attempt + 1}: {e}", exc_info=True)
					time.sleep(10)

			logging.error("Failed to generate content after multiple attempts.")
			return None

		except Exception as e:
			logging.error(f"Unexpected error in summarize_content: {e}", exc_info=True)
			return None
