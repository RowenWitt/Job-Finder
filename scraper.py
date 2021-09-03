from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

import pandas as pd
from bs4 import BeautifulSoup
import requests

# Turn whole damn thing into a class
# Salary is weird most of the time
# Description is weird <10% of the time
# Otherwise all good

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
#options.add_argument('--window-size=1260,1600')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options, executable_path="/usr/local/bin/chromedriver")

driver.get('https://www.indeed.com/jobs?q=data%20scientist&l=Los%20Angeles%2C%20CA')

driver.implicitly_wait(3)


job_card = driver.find_elements_by_xpath('//div[contains(@class,"mosaic-zone")]')

# Fix list indexing, probably by finding where not null, then dedupe later 
job_list = job_card[1].find_elements_by_xpath('./*[@id="mosaic-provider-jobcards"]')
jobs = job_list[0].find_elements_by_xpath('./*')

# turn into function for pagination
for job in jobs:
    try:
        listing = job.find_elements_by_xpath('//*[starts-with(@class, "tapItem")]')
        links = [elem.get_attribute('href') for elem in listing]
    except:
        print('fuck')


# Turn into function for each page
def get_page_info(data):
    start = time.time()
    total = []
    for role in data:
        driver.get(role)
        driver.implicitly_wait(2)

        indiv = {}
        # Find Title
        tit = driver.find_elements_by_xpath('//div[starts-with(@class, "jobsearch-JobInfoHeader-title-container")]')
        try:
            indiv['title'] = tit[0].text
        except:
            indiv['title'] = 'None'

        # Find Company
        comp = driver.find_elements_by_xpath('//div[starts-with(@class, "icl-u-xs-mt--xs")]')

        try:
            comp2 = comp[0].find_elements_by_xpath('./div[*]')
            try:
                indiv['company'] = comp2[0].text
            except:
                indiv['company'] = 'None'
        except:
            indiv['company'] = 'None'


        # Find Location
        try:
            loc = comp[0].find_elements_by_xpath('./.')
            loc2 = loc[0].find_elements_by_xpath('./.')

            indiv['location'] = loc2[0].text.split('\n')[1]
        except:
            indiv['location'] = 'None'

        # Find Reviews
        rev = driver.find_elements_by_xpath('//div[starts-with(@class, "icl-Ratings-starsCountWrapper")]')
        try:
            indiv['reviews'] = rev[0].get_attribute("aria-label")
        except:
            indiv['reviews'] = 'None'
            

        # Find Descriptions (Little weirdness here)
        desc = driver.find_elements_by_xpath('//div[@id="jobDescriptionText"]')
        try:
            desc2 = desc[0].find_elements_by_xpath('./*')
            text = ""
            for v in desc2:
                text += v.text

            indiv['description'] = text
        except:
            indiv['description'] = 'None'
            
            
        # Find Application Link
        try:
            app = driver.find_elements_by_xpath('//div[@id="applyButtonLinkContainer"]')
            app2 = app[0].find_elements_by_xpath('./*')
            app3 = app2[0].find_elements_by_xpath('./*')
            app4 = app3[0].find_elements_by_xpath('./*')

            indiv['app link'] = app4[0].get_attribute('href')
        
        except:
            indiv['app link'] = 'None'


        # Find Application Age
        try:
            age = driver.find_elements_by_xpath('//div[@class="jobsearch-JobMetadataFooter"]')
            age2 = age[0].find_elements_by_xpath('./div')
            if len(age2) == 3:
                indiv['age'] = age2[0].text
            elif len(age2) != 0:
                indiv['age'] = age2[1].text
            else:
                indiv['age'] = 'None'
        except:
            indiv['age'] = 'None'

                
        # Find Salary (Rare)
        try:
            sal = driver.find_elements_by_xpath('//span[@class="icl-u-xs-mr--xs"]')
            if len(sal) > 0:
                indiv['salary'] = sal[0].text
            else:
                indiv['salary'] = 'None'
        except:
            indiv['salary'] = 'None'


        total.append(indiv)

    print(time.time() - start)
    return total


test = get_page_info(links)


print(test)