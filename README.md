# Job-Finder
Scraper, ETL Pipeline, API for getting jobs from Indeed
Employs rotating user agent and proxies to avoid RL

- ChromeDriver version `93.0.4577.15`
- Python version `3.9.0`

## Known Defects

- Rotating proxies is annoying because many proxies are very slow -- time to scrape one page went from ~10 seconds to ~90 seconds.  Using minimal proxy rotation, long term solve is to pay for better proxies or run a couple proxies through AWS (I'm not willing to put the money into this).

- Entire app structure is heavily reliant upon try/except, which is not the same thing as clean code

- Currently takes about 10 seconds to scrape a page on my machine, probably not ideal

- Date posted is being stored in the database as the date of scraping minus the 'days since posted' from Indeed.  After 30 days this counter just says 'more than 30 days', this means that any job older than 30 days could be any number of days older than 30.  There's probably a better way

- Some job posts store descriptions in slightly different div location, could be managed through through an if statement

- reviews sometimes doesn't show up when it should, likely due to uncommon html structure

- If you want to build this into an app, you'll need a table to handle login info as well as a table relating `id` from JobListings table to a user's related actions.

- Missing a fair number of links to applications, a number of possible solutions, best is probably troubleshooting the scraper

- Scraper is making ~15x too many calls, could easily be fixed through rewrite

- DeDuplication is occuring by checking for a hashed value against a list of known hashed values, this could be improved

- Text is not being cleaned before DB input, had a reason for doing so but that reason is probably dumb

- Captcha is a problem, user-agent shuffling has been implemented, but paying for a captcha solving service is one solution, another might be to try and build a model to solve some captchas (this would not be easy).