from sqlalchemy import Table, Column, Integer, String, Date, Float, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from pyantic import BaseModel
from typing import Optional, List, Dict,


Base = declarative_base()


class JobListings(Base):

	__tablename__ == "job_listings"

	id = Column(Integer, primary_key=True, unique=True)
	company = Column(String(64))
	title = Column(String(128))
	location = Column(String(128))
	reviews = Column(String(64))
	link = Column(String(1024))
	date = Column(Date)
	salary = Column()
	description = Column(String(10000))

	def __repr__(self):
		return (
			"id:{}, company:{}, title:{}, location:{}, reviews:{}, link:{}, date:{}, salary:{}, description:{}").format(
			self.id,
			self.company,
			self.title,
			self.location,
			self.reviews,
			self.link,
			self.date,
			self.salary,
			self.description)