from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv)

import os

import app.pipeline

# # To be passed in as arguments
# root_url = os.getenv('ROOT_URL')
# driver_path = os.getenv('DRIVER_PATH')

# scraper = app.scraper.scraper(root_url, driver_path)

# data = scraper.scrape()
