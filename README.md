Predicting Housing Prices

> How frustrating is it when you want to look for houses to buy but you aren't sure where to begin. There are so many different factors that go into deciding when, where, and why to buy a house. 

> My goal is to build a recommender system that will hopefully make the process of looking for houses a bit easier. My hope is to use NLP on descriptions of houses you've already liked to cluster houses, along with different circumstances you're in, such as the size of family, job location, etc. to help you decide where you should live. 

## Structure:
> The website will take your favorited houses as csv format to recommend similar houses that may not be what you had been searching for originally but may be suitable for your circumstances. 

** NOTE: This can only be used with Redfin's formatted favorited houses as csv. **

## The way to retrieve your favorited houses in csv format:
1. Go to your Redfin favorites by clicking [here](https://www.redfin.com/myredfin/favorites).
2. Click on the 'Download' button that is to the left of the 'Map Homes' button.
3. Upload favorited houses as csv to the website.

## Information that can be entered:
* Number of bedrooms
* Number of bathrooms
* Desired square footage
* Price range
* Job location
* Max distance from job
* Children?

----
## Features of the model:
* zip-code: zip code of the house
* bedrooms: number of bedrooms in the house
* bathrooms: number of bathrooms in the house
* square footage: total square footage of the house
* date: date inquiry 
* year built: the year the house was built
* floors: number of floors in the house
* price: the price of the house for sale
* property type: townhouse, condo, home, etc
* location: the neighborhood of the house
* lot-size: size of the lot in acres
* days-on-market: number of days the house has been on the market

------

### Hopes for future of model

*In the future, I plan on building my dataset to reach cities outside of Washington as well as implementing an app to make this process more accessible*

----
## Updates

* May 17, 2018
	* All functions working and website is local

* May 15, 2018
	* Recommender is fully functional 

* May 10, 2018
	* Built baseline recommender based on users favorited houses
	* Began building deployment(html)

* May 9, 2018
	* Debugged clustering.py and update_data.py

* May 8, 2018
	* Created src directory (contains python files)
		* clustering.py (python file for clustering houses)
		* update_data.py (python file for updating the data)
	* Created notebooks directory (contains jupyter notebooks for EDA and webscraping)
		* EDA.ipynb
		* scraping-descriptions.ipynb

* May 7, 2018
	* First model 
	* Data collection

* April 26, 2018
	* Repo created
	* README.md created

----
### References:
See [Redfin](redfin.com) for reference to the data.