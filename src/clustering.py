import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from users import build_user_matrix

class Recommending:
    def __init__(self):
        '''Initializes the TFIDF Vectorizer Object'''

        self.tfidf = TfidfVectorizer(stop_words='english', max_features=100)
        self.results = {}

    def fit_transform(self, X, df):
        '''Fits and transforms TFIDF and fits KMeans.

        Params:
            X (array): Array of the descriptions of houses
            df (DataFrame): dataframe of numerical values to add
        Returns:
            tfidf_matrix (array): matrix with words, price, and beds as 
                features
        '''
        
        self.tfidf.fit(X)
        desc_tfidf = self.tfidf.transform(X)
        tfidf_matrix = pd.concat([pd.DataFrame(desc_tfidf.todense()),
                          df['PRICE'] / 1000, df['BEDS'], 
                          df['YEAR BUILT'] / 10], axis=1)
        return tfidf_matrix

    def cosine_sim(self, tfidf, df):
        ''' Creates a dictionary of the houses to consider based on cosine 
            similarity.
        
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

    def recommend(self, id):
        ''' Prints the recommendations for that house.
        
        Params:
            id (int): id of house that needs recommendations
            num (int): num of recommendations
        Returns:
            final_recs (list[tuples]): each item in the list is a 
                recommendation - each tuple is the score and the house id for 
                each recommendation
        '''

        recs = self.results[id]
        final_recs = []
        for rec in recs:
            if rec[0] > 0:
                final_recs.append(rec)
        return final_recs

    def item(self, id):
        ''' Helper method for returning item in dataframe when looking for 
            recommendations.

        Params:
            id (int): id of recommended house
        Returns:
            address (string): address of house that needs recommendations 
        '''

        return df.loc[df.index == id]['ADDRESS'].tolist()[0]


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
    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0', inplace=True, axis=1)
    df.drop_duplicates(inplace=True)
    for idx, row in df.iterrows():
        if row['PROPERTY TYPE'] == 'Vacant Land' and str(row['BEDS']) == 'NaN':
            df.loc[idx, 'BEDS'] = 0
            df.loc[idx, 'BATHS'] = 0
            df.loc[idx, 'SQUARE FEET'] = 0
            df.loc[idx, '$/SQUARE FEET'] = 0
    df['PRICE'] = df['PRICE'].dropna(axis=0)
    df = df.apply(lambda x:  x.fillna(x.mean()) if np.issubdtype(x.dtype, 
        np.number) else x.fillna(0),axis=0)    
    df['ID'] = df.reset_index(drop=True).index
    return df

def do_everything(file, orig_file='data/housing-data.csv'):
    '''Function that runs all necessary functions in file to work with app.py.
    
    Params:
        file (BytesIO obj or file path): csv like file that needs 
            recommendations 
        orig_file (file path): file path of all housing data
    Returns:
        recommendations ():
    '''
    df = get_data(orig_file, file)
    # build_user_matrix(df, file)
    recs = Recommending()
    tfidf = recs.fit_transform(df.DESC.values, df)
    recs.cosine_sim(tfidf, df)
    yes = df[df['FAVORITE'] == 'Y'].reset_index()
    recommend = pd.DataFrame()
    cur_recommendation = []
    houses = []
    scores = []
    for idx, item in yes.iterrows():
        house_id = item['ID']
        cur_recommendation.append(recs.recommend(house_id))
    for i, recs_ in enumerate(cur_recommendation):
        house_id = yes['ADDRESS'][i]
        for rec in recs_:
            new_row = df[df['ID'] == rec[1]]
            scores.append(round(rec[0], 3) - .17)
            houses.append(house_id)
            recommend = pd.concat([recommend, new_row], ignore_index=True)
    Score = pd.Series((scores), name='Score')
    favorited = pd.Series(houses, name='Favorited House')
    combination = pd.DataFrame([favorited, Score])
    recommendations = pd.concat([combination.T, recommend], axis=1)
    recommendations.drop(['DAYS ON MARKET', 'HOA/MONTH', 'ZIP', 
        'DESC', 'PRICE/SQUAREFT', 'SALE TYPE', 'SOLD DATE', 
        'STATUS','NEXT OPEN HOUSE START TIME', 'NEXT OPEN HOUSE END TIME', 
        'SOURCE', 'MLS#', 'FAVORITE', 'INTERESTED', 'LATITUDE', 'LONGITUDE',
        'LABEL', 'ID'], axis=1, inplace=True)
    return(recommendations)


if __name__ == '__main__':
    recs = do_everything('../data/favorites_test.csv', '../data/housing-data.csv')
    print(recs)
    # df = get_data('../data/housing-data.csv', '../data/favorites_test.csv')
    # recs = Recommending()
    # tfidf = recs.fit_transform(df.DESC.values, df)
    # recs.cosine_sim(tfidf, df)
    # recs.recommend(0, 2)
    # df = recs.result(df)
