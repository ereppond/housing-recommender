import pymongo
import pandas as pd
from selenium.webdriver import Chrome
from datetime.datetime import now
import os



class Data_Update:

	def __init__(self, old_data, new_data, sold=None):
		'''Initializes the self parameters.

		Params:
			old_data (filename): name of csv file for old data
			new_data (filename): name of csv file for new data
			sold (filename): name of csv file for sold houses

		'''

		self.df_old_data = pd.read_csv(old_data)
		self.old_data = old_data
		self.df_new_data = pd.DataFrame()
		self.new_data = new_data
		self.sold = sold


	def collect_new_data(self):
		'''Calls the webscraper that downloads necessary datasets.'''
		now = now()
		for idx, zipcode in enumerate(df_old_data['ZIP'].unique()):
			browser = Chrome()
			browser.get('https://www.redfin.com/zipcode/{}'.format(zipcode))
			download_button = browser.find_element_by_css_selector('a#download-and-save')
			download_button.click()
		
		directory = os.fsencode('/Users/elisereppond/Downloads')
		for file in os.listdir(directory):
		    filename = os.fsdecode(file)
		    month = now.month
		    day = now.day
		    if month <= 9:
		        month = '0{}'.format(month)
		    if day <= 9:
		        day = '0{}'.format(day)
		    if filename.startswith('redfin_{}-{}-{}'.format(now.year, month, day)):
		        self.df_new_data = pd.concat([self.df_new_data, 
		        	pd.DataFrame(filename)], axis=0)



	def compare_datasets(self):
		''' Moves houses to sold when no longer in new_data
		

		'''

# need to update every couple of days based on zipcodes
# scrape for new descriptions 
# move data that is no longer on market to sold database
# update aws
