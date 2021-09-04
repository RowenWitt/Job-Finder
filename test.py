from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os

import app.pipeline

# To be passed in as arguments

#root_url = os.getenv('ROOT_URL')
#root_url = 'https://www.indeed.com/jobs?q=data%20scientist&l=Las%20Vegas%2C%20NV'
#root_url = 'https://www.indeed.com/jobs?q=data%20scientist&l=San%20Francisco%2C%20CA'
root_url = 'https://www.indeed.com/jobs?q=data%20scientist&l=New%20York%2C%20NY'

driver_path = os.getenv('DRIVER_PATH')


pipe = app.pipeline.Pipeline(root_url, driver_path)

pipe.get_new_jobs(pages=5)


## Either add clicking to change location (easy)
## or rewrite scraper to pull all off one page
## how to deal with captcha???