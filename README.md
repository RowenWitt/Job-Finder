# Job-Finder
Scraper, ETL Pipeline, API for getting jobs from Indeed

## Known Defects

- Currently takes about 1 minute to scrape a page on my machine, probably not good

- Date posted is being stored in the database as the date of scraping minus the 'days since posted' from Indeed.  After 30 days this counter just says 'more than 30 days', this means that any job older than 30 days could be any number of days older than 30.  There's probably a better way
