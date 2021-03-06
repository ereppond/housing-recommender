# Housing Recommender

> How frustrating is it when you want to look for houses to buy but you aren't sure where to begin? There are so many different factors that go into deciding when, where, and why to buy a house. 

> My goal is to build a recommender system that will hopefully make the process of looking for houses a bit easier. I found the number of results to be frustrating because I wasn't necessarily set on one location. Therefore, I decided to build a system that would give me results in more than one location given my requirements for a house.

> I use Natural Language Processing on descriptions of houses, along with price, number of bedrooms, and the year the house was (or will be) built to find cosine similarity between houses to return new houses to you in order to help you decide where you should live. 

## Structure:
> The website will take your favorited houses as csv format to recommend similar houses that may not be what you had been searching for originally but may be suitable for your circumstances. 

** NOTE: This can only be used with Redfin's formatted favorited houses as csv. **

## The way to retrieve your favorited houses in csv format:
1. Go to your Redfin favorites by clicking [here](https://www.redfin.com/myredfin/favorites).
2. Click on the 'Download' button that is to the left of the 'Map Homes' button.
3. Upload favorited houses as csv to the website.

----

## Features of the recommender system:
* Tfidf Vectorizer
* Price (scaled)
* Number of bedrooms 
* Year house was built (scaled)


------

## Cloning the repo
After you have cloned the repo, you can use this code by doing the following:

1. Imports used in the code:
	* pandas
	* numpy
	* datetime
	* sklearn
	* os
	* time
	* random
	* selenium
	* flask
	* io

2. You should update the housing data by running 
``` python update_data.py <your_downloads_directory_path>```
Note: This will take a while to run

3. Once update_data is FINISHED running you can then run ``` python app.py ``` to see the website on your local computer


------

### Hopes for future of model

*In the future, I plan on building my dataset to reach cities outside of Washington as well as implementing an app to make this process more accessible. I am also hoping to implement a filtering system so the search can be even more refined*

#### Information that can be entered:
* Number of bedrooms
* Number of bathrooms
* Desired square footage
* Price range
* Job location
* Max distance from job
* Number of children

----
## Updates

* May 25, 2018
	* User friendly format corrected

* May 18, 2018
	* Pep8 Documentation fixed
	* Clean code

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


### Cloning the Repo
> Once you clone the repo, it is important to update the data before using the python files 


