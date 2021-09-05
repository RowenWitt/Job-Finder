from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os, time, re
import hashlib
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

			old_jobs = DB.get_JobListings_hashes()

			today = date.today()


			print(data)
			print(len(data))

			inputted = 0
			to_input = []
			for job in data:
				job['date'] = today
				num = re.sub('[^0-9]', '', job['age'])
				if num != '':
					job['date'] = today - timedelta(int(num))
				del job['age']


				to_hash = job['company'] + job['title']
				to_hash = to_hash.encode()
				h = hashlib.sha1(to_hash).hexdigest()
				job['hashed'] = h


				## job['app link'] != None and 
				if all(job['hashed'] != old.hashed for old in old_jobs):
					job['link'] = job['app link']
					del job['app link']
					to_input.append(job)
					inputted += 1

			logger.info('scraped {} new jobs'.format(len(to_input)))
			logger.info('inputted {} new jobs'.format(inputted))


			DB.insert_JobListings(to_input)


		### build schema dict to check against job

		### inspect JobListings to get table schema and check job against schema

