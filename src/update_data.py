import pymongo
import pandas as pd
from selenium.webdriver import Chrome
from datetime.datetime import now
import os



class Data_Update:

	def __init__(self, old_data):
		'''Initializes the self parameters.

		Params:
			old_data (filename): name of csv file for old data
			new_data (filename): name of csv file for new data

		'''

		self.df_old_data = pd.read_csv(old_data)
		self.df_new_data = pd.DataFrame()


	def collect_new_data(self):
		'''Calls the webscraper that downloads necessary datasets and
			adds them to dataframe.
		'''
		now = now()
		for idx, zipcode in enumerate(df_old_data['ZIP'].unique()):
			browser = Chrome()
			browser.get('https://www.redfin.com/zipcode/{}'.
				format(zipcode))
			download_button = browser.find_element_by_css_selector(
				'a#download-and-save')
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
		    if filename.startswith('redfin_{}-{}-{}'.format(now.year, month, 
		    	day)):
		        self.df_new_data = pd.concat([self.df_new_data, 
		        	pd.DataFrame(filename)], axis=0)
		self.df_new_data['DESC'] = ''


	def compare_datasets(self):
		''' Moves houses to sold when no longer in new_data.

		'''
		for idx_old, old_row in self.df_old_data.iterrows():
			for idx_new, new_row in self.df_new_data.iterrows():
				if old_row['ADDRESS'] == new_row['ADDRESS']:
					self.df_new_data['DESC'][idx_new] = old_row['DESC']


# update aws
