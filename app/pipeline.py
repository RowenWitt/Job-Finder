from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv)

import os

import app.scraper
import app.db

# To be passed in as arguments
root_url = os.getenv('ROOT_URL')
driver_path = os.getenv('DRIVER_PATH')

class Pipeline:

	def __init__(self, root_url, driver_path):
		self.root_url = root_url
		self.driver_path = driver_path


	def get_new_jobs(self, pages=5):
		""" runs `scraper` to get new jobs from indeed, cleans, inserts into `JobListings` """
		scraper = app.scraper.scrape(self.root_url, self.driver_path)

		data = scraper.scrape()

		clean_data = 




scraper = app.scraper.scraper(root_url, driver_path)

data = scraper.scrape()
