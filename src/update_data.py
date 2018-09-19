import os
import time
import random
import numpy as np
import pandas as pd
from selenium.webdriver import Chrome
from datetime import datetime


class Data_Update:

    def __init__(self, old_data='../data/housing-data.csv', dl_folder=
        '/Users/elisereppond/Downloads'):
        '''Initializes the class's parameters.

        Params:
            old_data (filename): name of csv file for old data
            dl_folder (folder): location where downloads are sent on local 
                computer
        '''

        self.df_old_data = pd.read_csv(old_data)
        self.df_old_data = self.df_old_data.rename(columns=
            {'URL (SEE http://www.redfin.com/buy-a-home/comparative-\
            market-analysis FOR INFO ON PRICING)': 'URL'})
        self.df_old_data.drop('Unnamed: 0', axis=1, inplace=True)
        self.df_new_data = pd.DataFrame()
        self.dl_folder = dl_folder

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
        ''' Collects the files from the Downloads folder and adds them to the 
            dataframe.
        '''

        print('collecting files')
        now = datetime.now()
        list_of_files = []
        directory = os.fsencode(self.dl_folder)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            print(filename)
            month = now.month
            day = now.day
            if month <= 9:
                month = '0{}'.format(month)
            if day <= 9:
                day = '0{}'.format(day)
            if filename.startswith('redfin_{}-{}-{}'.format(now.year, 
                month, day)):
                list_of_files.append(pd.read_csv('{}/{}'.format(self.dl_folder, filename)))
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
        self.df_new_data = self.df_new_data.drop(self.df_new_data['PRICE'].isnull(), axis=0)
        self.df_new_data.drop_duplicates(inplace=True)
        for idx, row in self.df_new_data.iterrows():
            if row['PROPERTY TYPE'] == 'Vacant Land':
                self.df_new_data.loc[idx, 'YEAR BUILT'] = datetime.now().year
                if str(row['BEDS']) == 'NaN':
                    self.df_new_data.loc[idx, 'BEDS'] = 0
                    self.df_new_data.loc[idx, 'BATHS'] = 0
                    self.df_new_data.loc[idx, 'SQUARE FEET'] = 0
                    self.df_new_data.loc[idx, '$/SQUARE FEET'] = 0
        self.df_new_data = self.df_new_data.apply(lambda x:  x.fillna(x.mean()) if np.issubdtype(x.dtype, 
            np.number) else x.fillna(0),axis=0)    
        self.df_new_data.reset_index(inplace=True, drop=True)
        self.df_new_data['ID'] = self.df_new_data.index
        '''***** note columns have been added such as ID'''


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

        self.df_new_data['DESC'].fillna('No Description', inplace=True)
        self.df_old_data = pd.concat([self.df_old_data,
            self.df_new_data]).drop_duplicates()
        self.df_old_data.to_csv('../data/old_data.csv')
        self.df_new_data.to_csv('../data/housing-data-new-test.csv')
    
    def data_html_format(self):
        ''' Puts the data into a format that looks nice on the website
            Note: at the end of this function it exports the new data into a file called final_html.csv in the data folder
        '''

        self.df_new_data.drop(self.df_new_data['PRICE'] == 0, axis=0, inplace=True)
        self.df_new_data['BEDS'] = self.df_new_data['BEDS'].astype(int)
        self.df_new_data['BATHS'] = self.df_new_data['BATHS'].apply(lambda x: str(x)[0:4] if str(x)[2] != '0' else int(x))
        self.df_new_data['HOA/MONTH'] = self.df_new_data['HOA/MONTH'].apply(lambda x: str(x)[0:4])
        html_data = self.df_new_data.copy()
        for idx, row in html_data.iterrows():
            html_data.loc[idx, 'ADDRESS'] = f"{str(row['ADDRESS'])} {row['CITY']} {row['STATE']} {str(row['ZIP'])}"
            html_data.loc[idx, 'PROPERTY TYPE'] = str(row['PROPERTY TYPE']) + ' ' + str(int(row['YEAR BUILT']))
        html_data = html_data[['PROPERTY TYPE', 'ADDRESS', 'LOCATION', 'PRICE', 'BEDS', 'BATHS', 'SQUARE FEET', 'LOT SIZE', 'DAYS ON MARKET', 'HOA/MONTH', 'URL']]
        html_data.dropna(inplace=True)
        html_data['DAYS ON MARKET'] = html_data['DAYS ON MARKET'].apply(lambda x: int(x))
        html_data['SQUARE FEET'] = html_data['SQUARE FEET'].apply(lambda x: str(x)[0:3])
        html_data['LOT SIZE'] = html_data['LOT SIZE'].apply(lambda x: int(x))
        html_data.to_csv('../final_html.csv')


if __name__ == '__main__':
    update = Data_Update('../data/housing-data.csv')
    update.collect_new_data()
    update.collecting_files() # need to use personal download directory
    update.compare_datasets()
    update.scraping_desc()
    update.replace_old_csv()
    update.data_html_format()
    print('DONE')