import app.scraper

# To be passed in as arguments
root_url = 'https://www.indeed.com/jobs?q=data%20scientist&l=Los%20Angeles%2C%20CA'
driver_path = '/usr/local/bin/chromedriver'

scraper = app.scraper.scraper(root_url, driver_path)

data = scraper.scrape()

print(data)