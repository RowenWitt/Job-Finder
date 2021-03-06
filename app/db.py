from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import json, os
from typing import Tuple, List, Dict

from sqlalchemy import create_engine, select, insert, update, func, inspect, and_
from sqlalchemy.orm import sessionmaker, scoped_session

from app.models import JobListings

db_url = os.getenv('DB_URL')

class Database(object):


	def __init__(self):
		self.engine = create_engine(
			db_url,
			pool_recycle=3600,
			pool_size=10,
			echo=False,
			pool_pre_ping=True
		)

		self.Sessionmaker = scoped_session(
			sessionmaker(
				autoflush=False,
				autocommit=False,
				bind=self.engine
			)
		)

		self.JobListings_schema = {
			'company':str,
			'title':str,
			'location':str,
			'reviews':str,
			'link':str,
			'date':str,
			'salary':str,
			'description':str
		}


	def init_JobListings(self):
		""" initializes JobListings table if not exists """

		insp = inspect(self.engine)
		if insp.has_table('job_listings') == False:
			JobListings.__table__.create(self.engine)


	def insert_JobListings(self, data: List[Dict]):
		""" inserts data into JobListings """
		with self.Sessionmaker() as session:
			last = select(func.max(JobListings.id))
			last_value = session.execute(last).fetchall()[0][0]
			for i in range(len(data)):
				if last_value is None:
					last_value = 0
				last_value += 1
				data[i]['id'] = last_value
				obj = JobListings(**data[i])
				session.add(obj)
				session.commit()



	def update_JobListings(self, data: List[Dict]):
		""" Updates Joblistings with data where id == id """
		with self.Sessionmaker() as session:

			for datum in data:
				query = (
					update(JobListings).
					where(JobListings.id == datum['id']).
					values(**datum)
				)
				session.execute(query)
				session.commit()



	def get_all_JobListings(self):
		""" SELECT * FROM job_listings """
		with self.Sessionmaker() as session:
			query = (
				select(JobListings)
			)
			data = session.execute(query).fetchall()

		return data



	def get_after_date_JobListings(self, date: str):   # Maybe this should be a datetime?
		""" SELECT * FROM job_listings WHERE date > input """
		with self.Sessionmaker() as session:
			query = (
				select(JobListings).
				where(JobListings.date >= date)
			)
			data = session.execute(query).fetchall()

		return data


	def get_JobListings_hashes(self):
		""" SELECT link FROM job_listings """
		with self.Sessionmaker() as session:
			query = (
				select(JobListings.hashed)
			)
			data = session.execute(query).fetchall()

		return data


	def get_all_JobListings_descriptions(self):
		""" gets all `id`s and `descriptions` from JobListings """
		with self.Sessionmaker() as session:
			query = (
				select(JobListings.id, JobListings.description)
			)
			data = session.execute(query).fetchall()

		return data


	def get_new_JobListings_descriptions(self):
		""" gets new `id`s and `descriptions` from JobListings """
		with self.Sessionmaker() as session:
			query = (
				select(JobListings.id, JobListings.description).
				where(JobListings.tokens == None)
			)
			data = session.execute(query).fetchall()

		return data



	def get_all_JobListings_tokens(self):
		""" Gets all tokens from JobListings """
		with self.Sessionmaker() as session:
			query = (
				select(JobListings.id, JobListings.tokens).
				order_by(JobListings.id)
			)
			data = session.execute(query).fetchall()

		return data

