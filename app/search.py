import app.db




DB = app.db.Database()


### Function to retrain KNN model




### Function to select a Job as a Seed and run KNN

	### Returns jobs in clean format




### Function to search by keywords KNN




### Function to get data from db based on certain subsets
	### City
	### Date Posted Range
	### Job Role Name





######### TO FIX #########


	### HIGH PRIORITY ###
## Need to fix text representations, easily could do it here, then update DB
## Probably is a better call to fix text before initial input, only doing it after because I was worried it would take a while


	### LOW PRIORITY ###
## Fix data input (salary, location, reviews)
## Maybe redesign scraper, currently going 1 page to 15 pages, could instead just get all data from 1 page (decrease calls by 15x)


	### Future Features ###
## Set up API to manage this automagically
## Set up some sort of frontend in Plotly dash / Flask
## Set up and LDA viz (how render???)
## See if frontend peeps want anything to do with the project




