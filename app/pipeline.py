from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os, time, re
from datetime import date, timedelta
import app.scraper
import app.db

DB = app.db.Database()

logger = app.scraper.logger

class Pipeline:

	def __init__(self, root_url, driver_path):
		self.root_url = root_url
		self.driver_path = driver_path


	def get_new_jobs(self, pages):
		""" runs `scraper` to get new jobs from indeed, cleans, inserts into `JobListings` """
		scraper = app.scraper.scraper(self.root_url, self.driver_path)

		data = scraper.scrape(depth=pages)

		if data is not None:

			data = [job for jobs in data for job in jobs]

			old_jobs = DB.get_JobListings_links()

			today = date.today()

			to_input = []
			for job in data:
				job['date'] = today
				num = re.sub('[^0-9]', '', job['age'])
				if num != '':
					job['date'] = today - timedelta(int(num))
				del job['age']

				## job['app link'] != None and 
				if job['date'] and all([(job['company'] != old.company and job['date'] != old.date) for old in old_jobs]):
					job['link'] = job['app link']
					del job['app link']
					to_input.append(job)

			logger.info('scraped {} new jobs'.format(len(to_input)))


			DB.insert_JobListings(to_input)


		### build schema dict to check against job

		### inspect JobListings to get table schema and check job against schema

