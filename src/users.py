from clustering import get_data
import pandas as pd

def build_user_matrix(df=None, new_user):
    ''' Adds new user data to users dataframe
    
    Params:
        df (DataFrame): dataframe of data (when called from clustering.py)
        new_user (file): df with favorited col updated for user
    Returns:
        users (DataFrame): pandas df of updated users
    '''
    
    users = pd.read_csv('../data/users.csv')
    if df == None:
        df = get_data('../data/housing-data.csv', new_user)
    house_id = list(users['house_id'])
    ratings = list(users['rating'])
    user_id = list(users['user_id'])
    df['rating'] = df['FAVORITE'].apply(lambda x: 1 if x == 'Y' else 0)
    df['user_id'] = df['FAVORITE'].apply(lambda x: (users.user_id.max() + 1) if x == 'Y' else 0)
    df = df.drop(df[df['user_id'] == 0].index)
    user_id.extend(list(df['user_id']))
    house_id.extend(list(df[df['FAVORITE'] == 'Y'].index))
    ratings.extend(list(df['rating']))
    users = pd.concat([pd.Series(user_id), pd.Series(house_id), pd.Series(ratings)], axis=1)
    users = users.rename(columns={0:'user_id', 1:'house_id', 2:'rating'})
    users.to_csv('../data/users.csv')
    return users