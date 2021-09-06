from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException

from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

import time, logging
import requests

import pandas as pd
from bs4 import BeautifulSoup
from random import choice

from app.agents import agents

# Salary is weird most of the time
# Description is weird <10% of the time
# Otherwise all good

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class scraper:

    def __init__(self, root_url, driver_path):
        self.agents = agents
        self.root_url = root_url
        self.driver_path = driver_path
        self.user_agent = choice(agents)
        self.options = webdriver.ChromeOptions()

        self.options.add_experimental_option("excludeSwitches", ["enable-automation"]) # Do I need these
        self.options.add_experimental_option("useAutomationExtension", False)  # Will this break

        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--window-size=1260,1600')
        self.options.add_argument('--headless')
        self.options.add_argument('user-agent={}'.format(self.user_agent))
        self.driver = webdriver.Chrome(options=self.options, executable_path=self.driver_path)


    def get_proxies(self):
        """ Get proxies from https://sslproxies.org """
        self.driver.get('https://sslproxies.org/')

        self.driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//table[@class='table table-striped table-bordered']//th[contains(., 'IP Address')]"))))

        ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(self.driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered']//tbody//tr/td[position() = 1]")))] # [@role='row']
        ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(self.driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered']//tbody//tr/td[position() = 2]")))] # [@role='row']
        self.driver.quit()
        proxies = []
        for i in range(0, len(ips)):
            proxies.append(ips[i]+':'+ports[i])

        return proxies


    def get_proxies_two(self):
        """ Get proxies from http-request-randomizer package (magic?) """
        req_proxy = RequestProxy()
        proxies = req_proxy.get_proxy_list()
        proxies = [proxy.get_address() for proxy in proxies]

        return proxies



    def get_a_proxy(self, proxies, root_url):
        """ attempts to use proxies until one is found with less than 2 second page load time """
        while True:
            new_proxy = choice(proxies)
            self.options.add_argument('--proxy-server={}'.format(new_proxy))
            self.driver = webdriver.Chrome(options=self.options, executable_path=self.driver_path)
            self.driver.set_page_load_timeout(5)
            try:
                self.driver.get(root_url)
                logger.info('selected working proxy {}'.format(new_proxy))
                self.driver.set_page_load_timeout(60)
                break
            except TimeoutException:
                self.driver.quit()
                del proxies[proxies.index(new_proxy)]
                logger.info('removed 1 bad proxy from proxy_list')
            except IndexError:
                logger.info('No more proxies to test')
                break
            except WebDriverException:
                logger.info('webDriverException, source unclear, removed bad proxy')
                del proxies[proxies.index(new_proxy)]

                        # new_proxy = choice(proxies)
            # try:
            #     self.driver.quit()
            # except:
            #     logger.info("driver error line 121 scraper.py")
            # logger.info("using {} proxy".format(new_proxy))

            # self.options.add_argument('--proxy-server={}'.format(new_proxy))
            # self.driver = webdriver.Chrome(options=self.options, executable_path=self.driver_path)
            # try:
            #     self.driver.get(role)
            # except:
            #     new_proxy = choice(proxies)
            #     self.options.add_argument('--proxy-server={}'.format(new_proxy))
            #     self.driver = webdriver.Chrome(options=self.options, executable_path=self.driver_path)




    def get_links_from_link(self, root_url):  # Switching proxy here as well wouldn't hurt
        """ Gets list of links leading to individual job posts from page of 15 job cards """
        self.driver = webdriver.Chrome(options=self.options, executable_path=self.driver_path)
        try:
            self.driver.get(root_url)
        except:
            logger.info('proxy went bad for some reason')
            return []
        new_agent = choice(agents)
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":new_agent})


        # self.driver.implicitly_wait(3) ## Testing speed without sp

        test = self.driver.find_elements_by_xpath('//div[contains(@class,"")]')
        # for i in test:
        #     print(i.text)
        print('test:', len(test))

        job_card = self.driver.find_elements_by_xpath('//div[contains(@class,"mosaic-zone")]')
        print('total elements:',len(job_card))

        # Fix list indexing, probably by finding where not null, then dedupe later 
        try:
            job_list = job_card[1].find_elements_by_xpath('./*[@id="mosaic-provider-jobcards"]')
            jobs = job_list[0].find_elements_by_xpath('./*')

            for job in jobs:
                try:
                    listing = job.find_elements_by_xpath('//*[starts-with(@class, "tapItem")]')
                    links = [elem.get_attribute('href') for elem in listing]
                except:
                    print('darn it')
                    links = ['darn it']



            return links
        except:
            logger.info("An Error Occured")


    def get_page_info(self, data):  # Probably want to switch proxy here at least
        """ Scrapes relevant info from job posts from each page of 15 jobs """
        start = time.time()
        total = []
        print('------ /n', len(data))
        for role in data:
            self.driver.get(role)
            try:
                self.driver.save_screenshot('SCRAPE.png')
            except:
                pass
            indiv = {}
            # Find Title
            tit = self.driver.find_elements_by_xpath('//div[starts-with(@class, "jobsearch-JobInfoHeader-title-container")]')
            try:
                indiv['title'] = tit[0].text
            except:
                print(tit)
                indiv['title'] = 'None'

            # Find Company
            comp = self.driver.find_elements_by_xpath('//div[starts-with(@class, "icl-u-xs-mt--xs")]')

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
            rev = self.driver.find_elements_by_xpath('//div[starts-with(@class, "icl-Ratings-starsCountWrapper")]')
            try:
                indiv['reviews'] = rev[0].get_attribute("aria-label")
            except:
                indiv['reviews'] = 'None'
                

            # Find Descriptions (Little weirdness here)
            desc = self.driver.find_elements_by_xpath('//div[@id="jobDescriptionText"]')
            try:
                indiv['description'] = desc[0].text
            except:
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
                app = self.driver.find_elements_by_xpath('//div[@id="applyButtonLinkContainer"]')
                app2 = app[0].find_elements_by_xpath('./*')
                app3 = app2[0].find_elements_by_xpath('./*')
                app4 = app3[0].find_elements_by_xpath('./*')

                indiv['app link'] = app4[0].get_attribute('href')
            
            except:
                indiv['app link'] = 'None'


            # Find Application Age
            try:
                age = self.driver.find_elements_by_xpath('//div[@class="jobsearch-JobMetadataFooter"]')
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
                sal = self.driver.find_elements_by_xpath('//span[@class="icl-u-xs-mr--xs"]')
                if len(sal) > 0:
                    indiv['salary'] = sal[0].text
                else:
                    indiv['salary'] = 'None'
            except:
                indiv['salary'] = 'None'


            total.append(indiv)

        logger.info('scraped 15 jobs in {} seconds'.format((time.time() - start)))
        return total


    def scrape(self, depth):
        """ gets 15 jobs per page, default is 5 pages of results """
        proxies = self.get_proxies()
        self.get_a_proxy(proxies, 'https://www.wikipedia.org')  # self.root_url

        self.driver.get('https://www.expressvpn.com/what-is-my-ip')
        self.driver.save_screenshot('IP.png')

        scraped = []
        
        for i in range(depth):
            if i == 0:
                page_url = self.root_url
            else:
                page_url = self.root_url + '&start={}'.format(i*10)
            print(page_url)
            links = self.get_links_from_link(page_url)  # 1 call 
            if links is not None:
                page = self.get_page_info(links) # 15 calls
                scraped.append(page)

            if i % 5 == 0:
                proxies = self.get_proxies()
                self.get_a_proxy(proxies, 'https://www.wikipedia.org')
        
        return scraped