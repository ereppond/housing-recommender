import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from users import build_user_matrix

class Recommending:
	def __init__(self, n_clusters=30):
		'''Initializes the TFIDF Vectorizer and KMeans Obj'''

		self.n_clusters = n_clusters
		self.tfidf = TfidfVectorizer(stop_words='english', max_features=100)
		self.km = KMeans(n_clusters=self.n_clusters)
		self.results = {}

	def fit_transform(self, X, df):
		'''Fits and transforms TFIDF and fits KMeans.

		Params:
			X (array): Array of the descriptions of houses
			df (DataFrame): dataframe of numerical values to add

		Returns:
			tfidf_matrix (array): matrix with words, 
				price, and beds as features
		'''
		
		self.tfidf.fit(X)
		desc_tfidf = self.tfidf.transform(X)
		self.km.fit(desc_tfidf.todense())
		tfidf_matrix = pd.concat([pd.DataFrame(desc_tfidf.todense()),
						  df['PRICE'] / 1000, df['BEDS']], axis=1)
		return tfidf_matrix

	def cosine_sim(self, tfidf, df):
		''' Creates a dictionary of the houses to consider based on cosine similarity.
		
		Params:
			tfidf (Tfidf object): object created in fit method
			df (DataFrame): dataframe for reference to address
		'''

		tfidf.fillna(0, inplace=True)
		cosine_similarities = cosine_similarity(tfidf,tfidf)
		for idx, row in df.iterrows():
			if idx < len(df):
				similar_indices = cosine_similarities[idx].argsort()[:-5:-1]
				similar_items = [(cosine_similarities[idx][i], i) for i in similar_indices]
				self.results[row['ID']] = similar_items[1:]

	def recommend(self, id, num):
		''' Prints the recommendations for that house.
		
		Params:
			id (int): id of house that needs recommendations
			num (int): num of recommendations
		'''

		recs = self.results[id][:num]
		final_recs = []
		for rec in recs:
			if rec[0] > 0:
				final_recs.append(rec)
		return final_recs[0]

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
		# build_user_matrix(df, fave_file)
	df['DESC'] = df['DESC'].fillna('No Description')
	df = df.fillna(0)
	if 'Unnamed: 0' in df.columns:
		df.drop('Unnamed: 0', inplace=True, axis=1)
	df.drop_duplicates(inplace=True)
	PROPERTY_TYPE = pd.get_dummies(df['PROPERTY TYPE'])
	df = pd.concat([df, PROPERTY_TYPE], axis=1)
	for idx, row in df.iterrows():
		if row['Vacant Land'] == 1 and str(row['BEDS']) == 'NaN':
			df.loc[idx, 'BEDS'] = 0
			df.loc[idx, 'BATHS'] = 0
			df.loc[idx, 'SQUARE FEET'] = 0
			df.loc[idx, '$/SQUARE FEET'] = 0
	df['BEDS'] = df['BEDS'].fillna(df['BEDS'].mean())
	df['PRICE'] = df['PRICE'].dropna(axis=0)
	df['ID'] = df.reset_index(drop=True).index
	return df

def do_everything(file):
	df = get_data('../data/housing-data.csv', file)
	recs = Recommending()
	tfidf = recs.fit_transform(df.DESC.values, df)
	recs.cosine_sim(tfidf, df)
	yes = df[df['FAVORITE'] == 'Y']
	recommend = [] #list of new rows 
	for idx, item in yes.iterrows():
		house_id = item['ID']
		cur_recommendation = recs.recommend(house_id, 1)
		row_of_rec = df[df['ID'] == house_id]
		other_info = {'Favorited House': item['ADDRESS'], 'Similarity Score': cur_recommendation[0] - 0.2}
		recommend.append(pd.concat([other_info, row_of_rec], axis=1))
	recommendations = pd.concat(recommend)
	return recommensations



if __name__ == '__main__':
	df = get_data('../data/housing-data.csv', '../data/favorites_test.csv')
	recs = Recommending()
	tfidf = recs.fit_transform(df.DESC.values, df)
	recs.cosine_sim(tfidf, df)
	recs.recommend(0, 2)
	df = recs.result(df)
	preds = recs.predictions(df)
	print(preds['ADDRESS'])
