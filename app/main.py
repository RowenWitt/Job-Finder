from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os

import app.pipeline

### How do I want to manage this...
# Probably a fast_api API