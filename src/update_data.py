import os
import time
import random
import numpy as np
import pandas as pd
from selenium.webdriver import Chrome
from datetime import datetime


class Data_Update:

	def __init__(self, old_data):
		'''Initializes the self parameters.

		Params:
			old_data (filename): name of csv file for old data
			new_data (filename): name of csv file for new data
		'''

		self.df_old_data = pd.read_csv(old_data)
		self.df_old_data = self.df_old_data.rename(columns=
			{'URL (SEE http://www.redfin.com/buy-a-home/comparative-\
			market-analysis FOR INFO ON PRICING)': 'URL'})
		self.df_new_data = pd.DataFrame()


	def collect_new_data(self):
		'''Calls the webscraper that downloads necessary datasets.
		'''

		browser = Chrome()
		for idx, zipcode in enumerate(self.df_old_data['ZIP'].unique()):
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

		print('collecting files')
		now = datetime.now()
		list_of_files = []
		directory = os.fsencode('/Users/elisereppond/Downloads')
		for file in os.listdir(directory):
			filename = os.fsdecode(file)
			month = now.month
			day = now.day
			if month <= 9:
				month = '0{}'.format(month)
			if day <= 9:
				day = '0{}'.format(day)
			if filename.startswith('redfin_{}-{}-{}'.format(now.year, 
				month, day)):
				list_of_files.append(pd.read_csv('/Users/elisereppond/Downloads/{}'.\
					format(filename)))
		try: 
			self.df_new_data = pd.concat(list_of_files, axis=0)
			print('concatinated files')
		except ValueError:
			self.df_new_data = self.df_old_data
			print('COULD NOT CONCATINATE FILES')
		self.clean_data()
		self.df_new_data = self.df_new_data.reset_index().drop('index', axis=1)


	def clean_data(self):
		''' Cleans the data to match the proper format necessary for 
		modeling.
		'''

		print('cleaning')
		self.df_new_data['DESC'] = 'No Description'
		self.df_new_data = self.df_new_data.rename(columns=
			{'URL (SEE http://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)': 
			'URL', 
			'$/SQUARE FEET': 'PRICE/SQUAREFT'})
		self.df_new_data.drop(self.df_new_data[self.df_new_data['STATE']
			!= 'WA'].index, inplace=True)
	    self.df_new_data['PRICE'] = self.df_new_data['PRICE'].dropna(axis=0)
		self.df_new_data.drop_duplicates(inplace=True)
		for idx, row in self.df_new_data.iterrows():
	        if row['PROPERTY TYPE'] == 'Vacant Land':
	            self.df_new_data.loc[idx, 'YEAR BUILT'] = datetime.now().year
	            if str(row['BEDS']) == 'NaN':
	                self.df_new_data.loc[idx, 'BEDS'] = 0
	                self.df_new_data.loc[idx, 'BATHS'] = 0
	                self.df_new_data.loc[idx, 'SQUARE FEET'] = 0
	                self.df_new_data.loc[idx, '$/SQUARE FEET'] = 0
	    self.df_new_data['LABEL'] = 0
	    df = df.apply(lambda x:  x.fillna(x.mean()) if np.issubdtype(x.dtype, 
	    	np.number) else x.fillna(0),axis=0)    
    	df['ID'] = df.reset_index(drop=True).index
		'''***** note columns have been added such as ID
			and label column needs to be removed once the 
			original data has been altered'''


	def compare_datasets(self):
		''' Adds the descriptions to the new data from the 
		old data where the address is the same.
		'''

		for idx_new, new_row in self.df_new_data.iterrows():
			if str(new_row['ADDRESS']) in np.array(self.df_old_data['ADDRESS']):
				ind = self.df_old_data.index[self.df_old_data['ADDRESS'] == str(new_row['ADDRESS'])].tolist()
				self.df_new_data.loc[idx_new,'DESC'] = self.df_old_data.loc[ind[0], 'DESC']
				if idx_new % 100 == 0:
					print('comparing datasets on line {} / {}'.format(idx_new, self.df_new_data.shape[0]))


	def scraping_desc(self):
		''' Scrapes descriptions for descriptions of houses recently 
		added to data.
		'''

		i = 0
		while len(self.df_new_data[self.df_new_data['DESC'] == 'No Description']) > 50 and i < 20:
			i += 1
			print(len(self.df_new_data[self.df_new_data['DESC'] == 'No Description']))
			browser = Chrome()
			for idx, row in self.df_new_data.iterrows():
				if (str(row['DESC']) == 'No Description') or (str(row['DESC']) == 
					'NaN'):
					url = row['URL']
					try:
						browser.get(url)
						sel = "div.sectionContent"
						description = browser.find_elements_by_css_selector(sel)
						self.df_new_data.loc[idx,'DESC'] = description[0].text
						time.sleep(2 + random.random() * 3)
					except IndexError:
						self.df_new_data.loc[idx,'DESC'] = 'No Description'
					except: 
						pass

	def replace_old_csv(self):
		''' Replaces the old csv files with the updated ones.'''

		self.df_new_data['LABEL'] = 0
		self.df_new_data['DESC'].fillna('No Description', inplace=True)

		if self.df_old_data.columns.sort() == self.df_new_data.columns.sort(): 
			self.df_old_data = pd.concat([self.df_old_data,
				self.df_new_data]).drop_duplicates()
			print('concatinated old and new df')
		else:
			print('couldnt concatinate old and new df for exporting')
		self.df_old_data.to_csv('../data/old_data.csv')
		self.df_new_data.to_csv('../data/housing-data-new-test.csv')


if __name__ == '__main__':
	update = Data_Update('../data/housing-data.csv')
	update.collect_new_data()
	update.collecting_files()
	update.compare_datasets()
	update.scraping_desc()
	update.replace_old_csv()
	print('DONE')