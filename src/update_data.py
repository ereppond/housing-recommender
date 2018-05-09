import pymongo
import pandas as pd
from selenium.webdriver import Chrome
from datetime import datetime
import os



class Data_Update:

	def __init__(self, recent_data, old_data):
		'''Initializes the self parameters.

		Params:
			old_data (filename): name of csv file for old data
			new_data (filename): name of csv file for new data

		'''
		self.df_old_data = pd.read_csv(old_data)
		self.df_recent = pd.read_csv(recent_data)
		self.df_new_data = pd.DataFrame()


	def collect_new_data(self):
		'''Calls the webscraper that downloads necessary datasets and
			adds them to dataframe.
		'''
		now = datetime.now()
		for idx, zipcode in enumerate(self.df_recent['ZIP'].unique()):
			browser = Chrome()
			try:
				browser.get('https://www.redfin.com/zipcode/{}'.
					format(zipcode))
				download_button = browser.find_element_by_css_selector(
					'a#download-and-save')
				download_button.click()
			except:
				pass
		
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
		return self.df_new_data


	def compare_datasets(self):
		''' Moves houses to sold when no longer in new_data.

		'''
		for idx_old, old_row in self.df_recent.iterrows():
			for idx_new, new_row in self.df_new_data.iterrows():
				if old_row['ADDRESS'] == new_row['ADDRESS']:
					self.df_new_data.loc[idx,'DESC'] = old_row['DESC']


	def scraping_desc(self):
		''' Scrapes descriptions for descriptions of houses recently added to data'''
		for idx, row in self.df_new_data.iterrows():
			if row['DESC'] == '':
				url = row['URL']
				try:
					browser.get(url)
					sel = "div.sectionContent"
					description = browser.find_elements_by_css_selector(sel)
					self.df_new_data.loc[idx,'DESC'] = description
				except:
					self.df_new_data.loc[idx,'DESC'] = 'No Description'

	def replace_old_csv(self):
		self.df_old_data = pd.concat([df_recent, df_old_data], ignore_index=True)
		self.df_old_data.to_csv('../data/old_data.csv')
		self.df_new_data.to_csv('../data/housing-data.csv')


if __name__ == '__main__':
	update = Data_Update('../data/old_data.csv', '../data/housing-data.csv')
	update.collect_new_data()
	update.compare_datasets()
	update.scraping_desc()
	print(update.df_new_data.DESC)
	# update.replace_old_csv()