import app.db
from app.scraper import logger

import time
import spacy
from bs4 import BeautifulSoup


class search:

	def __init__(self):
		self.DB = app.db.Database()
		self.nlp = spacy.load('en_core_web_sm')



	def clean_strings(self):
		""" function to clean dirty strings within the database """

		print('write function 1')



	def tokenizer(self, data):
		""" tokenizes one string, data input is a tuple of (id, text) """
		tokens = []
		for token in self.nlp(data[1]):
			if (token.is_stop != True) & (token.is_punct != True) & (token.is_space != True) & (token.is_digit != True):
				tokens.append(token.lemma_.lower())
		tokens = " ".join(tokens)
		data_tuple = (data[0], tokens)
		return data_tuple



	def create_tokens(self, retro=False):
		""" tokenizes text and updates `tokens` column in DB, retro=True updates existing tokens, False only new tokens """
		start = time.time()

		if retro == True:
			tokens_objects = self.DB.get_all_JobListings_descriptions()
		else:
			tokens_objects = self.DB.get_new_JobListings_descriptions()

		token_tuple_list = [{'id':token_id_tuple[0], 'tokens':self.tokenizer(token_id_tuple)[1]} for token_id_tuple in tokens_objects]


		logger.info('tokenized {} strings in {} seconds'.format(len(token_tuple_list), (time.time() - start)))
		return token_tuple_list



	def update_tokens(self, retro=False):
		""" Updates rows where id == id with new tokens """
		start = time.time()

		tokens = self.create_tokens(retro=retro)

		self.DB.update_JobListings(tokens)

		logger.info('updated {} rows in {} seconds'.format(len(tokens), (time.time() - start)))





### Function to retrain KNN model




### Function to select a Job as a Seed and run KNN

	### Returns jobs in clean format




### Function to search by keywords KNN




### Function to get data from db based on certain subsets
	### City
	### Date Posted Range
	### Job Role Name





######### TO FIX #########


	### HIGH PRIORITY ###
## Need to fix text representations, easily could do it here, then update DB
## Probably is a better call to fix text before initial input, only doing it after because I was worried it would take a while


	### LOW PRIORITY ###
## Fix data input (salary, location, reviews)
## Maybe redesign scraper, currently going 1 page to 15 pages, could instead just get all data from 1 page (decrease calls by 15x)


	### Future Features ###
## Set up API to manage this automagically
## Set up some sort of frontend in Plotly dash / Flask
## Set up and LDA viz (how render???)
## See if frontend peeps want anything to do with the project




