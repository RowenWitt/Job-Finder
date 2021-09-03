# Job-Finder
Scraper, ETL Pipeline, API for getting jobs from Indeed

- ChromeDriver version `93.0.4577.15`

## Known Defects

- Currently takes about 1 minute to scrape a page on my machine, probably not good

- Date posted is being stored in the database as the date of scraping minus the 'days since posted' from Indeed.  After 30 days this counter just says 'more than 30 days', this means that any job older than 30 days could be any number of days older than 30.  There's probably a better way

- Some job posts store descriptions in slightly different div location, could be managed through through an if statement

- If you want to build this into an app, you'll need a table to handle login info as well as a table relating `id` from JobListings table to a user's related actions.