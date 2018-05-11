import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Recommending:
	def __init__(self, n_clusters=30):
		'''Initializes the TFIDF Vectorizer and KMeans Obj'''

		self.n_clusters = n_clusters
		self.tfidf = TfidfVectorizer(stop_words='english', max_features=300)
		self.km = KMeans(n_clusters=self.n_clusters)
		self.results = {}

	def fit_transform(self, X):
		'''Fits and transforms TFIDF and fits KMeans.

		Params:
			X (array): Array of the descriptions of houses

		'''
		self.tfidf.fit(X)
		desc_tfidf = self.tfidf.transform(X)
		self.km.fit(desc_tfidf.todense())
		return desc_tfidf

	def cosine_sim(self,tfidf):
		''' Creates a dictionary of the houses to consider based on cosine similarity.
		
		Params:
			tfidf (Tfidf object): object created in fit method
		'''
		
		cosine_similarities = cosine_similarity(tfidf,tfidf)
		for idx, row in df.iterrows():
			if idx < 2822:
				similar_indices = cosine_similarities[idx].argsort()[:-5:-1]
				similar_items = [(cosine_similarities[idx][i], i) for i in similar_indices]
				self.results[row['ID']] = similar_items[1:]

	def recommend(self, id, num):
		''' Prints the recommendations for that house.
		
		Params:
			id (int): id of house that needs recommendations
			num (int): num of recommendations
		'''
		
		try:
			if (num == 0):
				print("Unable to recommend any house")
			elif (num==1):
				print("Recommending " + str(num) + " house similar to " + self.item(id))
			else :
				print("Recommending " + str(num) + " houses similar to " + self.item(id))

			print("----------------------------------------------------------")
			recs = self.results[id][:num]
			for rec in recs:
				print("You may also like to look at: " + self.item(rec[1]) + " (score:" + str(rec[0]) + ")")
		except IndexError:
			print('These are the houses most similar to your house')
			pass

	def item(self, id):
		''' Helper method for returning item in dataframe when looking for recommendations.
		
		Params:
			id (int): id of recommended house
		'''
		
		return df.loc[df.index == id]['ADDRESS'].tolist()[0]



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
		possible_clusters = df[df['FAVORITE'] == 'Y']['LABEL'].unique()
		for idx, row in df.iterrows():
			if row['LABEL'] in possible_clusters and row['FAVORITE'] == 'N':
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
				df.loc[idx,'FAVORITE'] = 'Y'
	df['DESC'] = df['DESC'].fillna('No Description')
	df = df.fillna(0)
	if 'Unnamed: 0' in df.columns:
		df.drop('Unnamed: 0', inplace=True, axis=1)
	df.drop_duplicates(inplace=True)
	df['ID'] = df.index
	return df


if __name__ == '__main__':
	df = get_data('../data/housing-data.csv', '../data/favorites_test.csv')
	recs = Recommending()
	tfidf = recs.fit_transform(df.DESC.values)
	recs.cosine_sim(tfidf)
	recs.recommend(0, 2)
	df = recs.result(df)
	preds = recs.predictions(df)
	print(preds['ADDRESS'])
