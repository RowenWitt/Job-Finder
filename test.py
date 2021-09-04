from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os

import app.pipeline

# To be passed in as arguments
root_url = os.getenv('ROOT_URL')
driver_path = os.getenv('DRIVER_PATH')


pipe = app.pipeline.Pipeline(root_url, driver_path)

pipe.get_new_jobs(pages=10)


