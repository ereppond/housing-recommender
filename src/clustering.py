from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
# import pymongo


class Clustering:

	def __init__(self, n_clusters=30)
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


def get_training_data(file)
	'''Takes in a filename and returns it as a dataframe


	Params:
		file (csv): file in csv format

	Returns:
		df (DataFrame): pandas dataframe of data from file
	'''
	return pd.read_csv(file)


if __name__ == '__main__':
	df = get_training_data()
	cluster = Clustering()
	cluster.fit_transform(df.DECS.values)
	df = cluster.result(df)
	return df
	