from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
# import pymongo


class Clustering:

	def __init__(self, n_clusters=30):
		'''Initializes the TFIDF Vectorizer and KMeans Obj'''
		self.n_clusters = n_clusters
		self.tfidf = TfidfVectorizer(stop_words='english', max_features=50)
		self.km = KMeans(n_clusters=30)
	

	def fit_transform(self, X):
		'''Fits and transforms TFIDF and fits KMeans
		
		Params:
			X (array): Array of the descriptions of houses

		'''
		self.tfidf.fit(X)
		desc_tfidf = tfidf.transform(X)
		self.km.fit(desc_tfidf.todense())


	def result(self, df):
		'''Takes the df and builds a column with the labels for each house

		Params:
			df (DataFrame): dataframe with all the housing data

		
		Returns:
			df (DataFrame): dataframe including new column for label

		'''
		df['labels'] = pd.Series(self.km.labels_)
		return df


def get_training_data(file, fave_file=None):
	'''Takes in a filename and returns it as a dataframe


	Params:
		file (csv): file in csv format

	Returns:
		df (DataFrame): pandas dataframe of data from file
	'''
	df_all_data = pd.read_csv(file)
	if fave_file != None:
		df_faves = pd.read_csv(fave_file)
		for idx, row in df_all_data.iterrows():
			if row['ADDRESS'] in df_faves['ADDRESS']:
				row['FAVORITE'] = 'Y'
	df_all_data.drop(['NEXT OPEN HOUSE DATE', 'NEXT OPEN HOUSE START TIME', 
		'NEXT OPEN HOUSE END TIME'])
	return 


if __name__ == '__main__':
	df = get_training_data('housing_data.csv', 'favorites.csv')
	cluster = Clustering()
	cluster.fit_transform(df.DECS.values)
	df = cluster.result(df)
	return df
