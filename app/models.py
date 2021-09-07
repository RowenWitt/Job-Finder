from sqlalchemy import Table, Column, Integer, String, Date, Float, Boolean, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional, List, Dict


Base = declarative_base()


class JobListings(Base):

	__tablename__ = "job_listings"

	id = Column(Integer, primary_key=True, unique=True)
	hashed = Column(String(40))
	company = Column(String(128))
	title = Column(String(128))
	location = Column(String(128))
	reviews = Column(String(64))
	link = Column(String(4096))
	date = Column(Date)
	salary = Column(String(128))
	description = Column(Text)
	tokens = Column(Text)

	def __repr__(self):
		return (
			"id:{}, company:{}, title:{}, location:{}, reviews:{}, link:{}, date:{}, salary:{}, description:{}, tokens:{}").format(
			self.id,
			self.company,
			self.title,
			self.location,
			self.reviews,
			self.link,
			self.date,
			self.salary,
			self.description,
			self.tokens)