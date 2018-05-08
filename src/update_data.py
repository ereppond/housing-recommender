import pymongo
import pandas as pd

class Data_Update:

	def __init__(self, old_data, sold):
		self.old_data = old_data
		self.sold = sold

# need to update every couple of days based on zipcodes
# scrape for new descriptions 
# move data that is no longer on market to sold database
# update mongodb
