import pymongo
import pandas as pd
from selenium.webdriver import Chrome
from datetime import datetime
import os
import time
import random


class Data_Update:

	def __init__(self, recent_data, old_data):
		'''Initializes the self parameters.

		Params:
			old_data (filename): name of csv file for old data
			new_data (filename): name of csv file for new data

		'''
		self.df_old_data = pd.read_csv(old_data)
		self.df_old_data = self.df_old_data.rename(columns=
			{'URL (SEE http://www.redfin.com/buy-a-home/comparative-\
			market-analysis FOR INFO ON PRICING)': 'URL'})
		self.df_recent = pd.read_csv(recent_data)
		self.df_recent = self.df_recent.rename(columns=
			{'URL (SEE http://www.redfin.com/buy-a-home/comparative-\
			market-analysis FOR INFO ON PRICING)': 'URL'})
		self.df_new_data = pd.DataFrame()


	def collect_new_data(self):
		'''Calls the webscraper that downloads necessary datasets.
		'''

		browser = Chrome()
		for idx, zipcode in enumerate(self.df_recent['ZIP'].unique()):
			try:
				browser.get('https://www.redfin.com/zipcode/{}'.
					format(zipcode))
				time.sleep(1 + random.random() * 3)
				download_button = browser.find_element_by_css_selector(
					'a#download-and-save')
				download_button.click()
			except:
				pass

	def collecting_files(self):
		''' Collects the files from the Downloads folder and adds 
		them to the dataframe.
		'''

		now = datetime.now()
		list_of_files = []
		directory = os.fsencode('/Users/elisereppond/Downloads')
		for file in os.listdir(directory):
			filename = os.fsdecode(file)
			month = 5
			day = 9
			if month <= 9:
				month = '0{}'.format(month)
			if day <= 9:
				day = '0{}'.format(day)
			if filename.startswith('redfin_{}-{}-{}'.format(now.year, month, 
				day)):
				list_of_files.append(pd.read_csv('/Users/elisereppond/Downloads/{}'.\
					format(filename)))
		self.df_new_data = pd.concat(list_of_files)
		self.df_new_data = self.clean_data()


	def clean_data(self):
		''' Cleans the data to match the proper format necessary for 
		modeling.
		'''

		self.df_new_data['DESC'] = 'No Description'
		self.df_new_data = self.df_new_data.rename(columns=
			{'URL (SEE http://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)': 
			'URL', 
			'$/SQUARE FEET': 'PRICE/SQUAREFT'})
		self.df_new_data['SALE TYPE'] = self.df_new_data['SALE TYPE'].apply(
			lambda x: 1 if x == 'MLS Listing' or x == 'For-Sale-by-Owner Listing' 
			else 0)
		self.df_new_data.drop(self.df_new_data[self.df_new_data['STATE']
			!= 'WA'].index, inplace=True)
		# self.df_new_data.drop(['SOLD DATE', ])
		return self.df_new_data	



	def compare_datasets(self):
		''' Adds the descriptions to the new data from the 
		old data where the address is the same.
		'''

		for idx_old, old_row in self.df_recent.iterrows():
			for idx_new, new_row in self.df_new_data.iterrows():
				if old_row['ADDRESS'] == new_row['ADDRESS']:                    
					self.df_new_data.loc[idx_new,'DESC'] = old_row['DESC']


	def scraping_desc(self):
		''' Scrapes descriptions for descriptions of houses recently 
		added to data.
		'''

		for idx, row in self.df_new_data.iterrows():
			if row['DESC'] == 'No Description':
				url = row['URL']
				try:
					browser.get(url)
					sel = "div.sectionContent"
					description = browser.find_elements_by_css_selector(sel)
					self.df_new_data.loc[idx,'DESC'] = description
				except:
					self.df_new_data.loc[idx,'DESC'] = 'No Description'

	def replace_old_csv(self):
		''' Replaces the old csv files with the updated ones.'''

		self.df_new_data['LABEL'] = 0
		self.df_new_data = pd.concat([self.df_old_data, self.df_recent, 
			self.df_new_data]).drop_duplicates(axis=0)
		self.df_new_data['ID'] = self.df_new_data.index
		self.df_old_data.to_csv('../data/old_data.csv')
		self.df_new_data.to_csv('../data/housing-data-new-test.csv')


if __name__ == '__main__':
	update = Data_Update('../data/old_data.csv', '../data/housing-data.csv')
	# update.collect_new_data()
	update.collecting_files()
	update.compare_datasets()
	update.scraping_desc()
	update.replace_old_csv()
	print('DONE')