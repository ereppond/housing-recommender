import pandas as pd

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer



class Clustering:
	def __init__(self, n_clusters=60):
		'''Initializes the TFIDF Vectorizer and KMeans Obj'''

		self.n_clusters = n_clusters
		self.tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
		# self.km = KMeans(n_clusters=self.n_clusters)


	def fit_transform(self, X):
		'''Fits and transforms TFIDF and fits KMeans.
		
		Params:
			X (array): Array of the descriptions of houses

		'''
		self.tfidf.fit(X)
		desc_tfidf = self.tfidf.transform(X)
		return desc_tfidf
		# print(desc_tfidf.shape)
		# self.km.fit(desc_tfidf.todense())


	def result(self, df):
		'''Takes the df and builds a column with the labels for each house.

		Params:
			df (DataFrame): dataframe with all the housing data

		
		Returns:
			df (DataFrame): dataframe including new column for label

		'''
		df['LABEL'] = pd.Series(self.km.labels_)
		return df

	def predictions(self, df):
		'''Returns houses that are in the same clusters as their favorites.

		Params:
			df (DataFrame): entire dataframe with the favorites and the cluster labels

		Returns:
			pos (DataFrame): dataframe of houses that have similar descriptions 
				to those that they favorited

		'''
		list_of_rows = []
		possible_clusters = df[df['FAVORITED'] == 'Y']['LABEL'].unique()
		for idx, row in df.iterrows():
			if row['LABEL'] in possible_clusters and row['FAVORITED'] == 'N':
				list_of_rows.append(row)
		return pd.concat(list_of_rows)



def get_data(file, fave_file=None):
	'''Takes in a filename and returns it as a dataframe.


	Params:
		file (csv): file in csv format

	Returns:
		df (DataFrame): pandas dataframe of data from file
	'''
	df = pd.read_csv(file)
	df['FAVORITE'] = 'N'
	if fave_file != None:
		df_faves = pd.read_csv(fave_file)
		for idx, row in df.iterrows():
			if row['ADDRESS'] in list(df_faves['ADDRESS']):
				df.loc[idx,'FAVORITE'] = df['FAVORITE'].max() + 1
	df['DESC'] = df['DESC'].fillna('No Description')
	df = df.fillna(0)
	if 'Unnamed: 0' in df.columns:
		df.drop('Unnamed: 0', inplace=True, axis=1)
	df.drop_duplicates(inplace=True)
	return df


if __name__ == '__main__':
	df = get_data('../data/housing-data.csv', '../data/favorites_test.csv')
	cluster = Clustering()
	cluster.fit_transform(df.DESC.values)
	print(df.shape)
	df = cluster.result(df)
	preds = cluster.predictions(df)
	print(preds['ADDRESS'])
