"""
* Note: pages ordered by what appears on the navigation bar at the top of the website
"""
from flask import (Flask,
                   jsonify,
                   render_template,
                   request,
                   redirect, 
                   url_for)
import tablib
from io import BytesIO
import os
import pandas as pd
from src.clustering import do_everything

# from ec2.prophet_db import web_query

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    '''Main page of website that gives access to the rest of the attributes of the page.

    Returns:
        index.html (html template): main page template
    '''

    if request.method == 'POST':
        return redirect(url_for('uploadajax'))
    return render_template('index.html')


@app.route('/uploadajax', methods=['POST'])
def uploadajax():
    '''File that is processed in the ajax function at the beginning of the recommendations page.

    Returns: 
        uploaded_file.html (html template): template for what is displayed once the uploaded file has been processed.
    '''

    file = request.files['file']
    f = BytesIO()
    file.save(f)
    f.seek(0)
    df = do_everything(f)  # returns pandas df with table to display 
    list_of_vals = [list(df[i].values) for i in df]
    columns = df.columns
    return render_template('uploaded_file.html', data=zip(*list_of_vals), columns=columns)


@app.route('/data', methods=['GET', 'POST'])
def data():
    '''Data page to display what the data looks like on the end of the recommender system.
    
    * Note: this function calls a function 'do_everything' from clustering.py that does 
        everything in order to make the recommender system run.

    Returns:
        
    '''
    df = pd.read_csv('data/final_html.csv')
    df.drop('Unnamed: 0', axis =1, inplace=True)
    df.fillna(0, inplace=True)
    list_of_vals = [list(df[i].values) for i in df]
    columns = df.columns
    return render_template('data.html', data=zip(*list_of_vals), columns=columns)

@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    # Favorites page to explain how to get the favorited csv file
    return render_template('favorites.html')


@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    return render_template('recommendations.html') 


@app.route('/uploaded_file', methods = ['GET', 'POST'])
def uploaded_file():
    #for uploading file 
    return render_template('uploaded_file.html')


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    # Welcome page to explain what is going on in the site
    return render_template('welcome.html')


# @app.route('/table')
# def table():
#     df = pd.read_csv('data/final_html.csv')
#     df.drop('Unnamed: 0', axis =1, inplace=True)
#     df.fillna(0, inplace=True)
#     list_of_vals = [list(df[i].values) for i in df]
#     columns = df.columns
#     return render_template('tabulator-table.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

