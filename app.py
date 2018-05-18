"""
Simple flask app.
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


@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    return render_template('recommendations.html') 


@app.route('/uploadajax', methods=['POST'])
def uploadajax():
    file = request.files['file']
    f = BytesIO()
    file.save(f)
    f.seek(0)
    df = do_everything(f)  # returns pandas df with table to display 
    list_of_vals = [list(df[i].values) for i in df]
    columns = df.columns
    return render_template('uploaded_file.html', data=zip(*list_of_vals), columns=columns)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('uploadajax'))
    return render_template('index.html')


@app.route('/table')
def table():
    df = pd.read_csv('data/final_html.csv')
    df.drop('Unnamed: 0', axis =1, inplace=True)
    df.fillna(0, inplace=True)
    list_of_vals = [list(df[i].values) for i in df]
    columns = df.columns
    return render_template('tabulator-table.html')

@app.route('/uploaded_file', methods = ['GET', 'POST'])
def uploaded_file():
    #for uploading file 
    return render_template('uploaded_file.html')



@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    # Welcome page to explain what is going on in the site
    return render_template('welcome.html')


@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    # Favorites page to explain how to get the favorited csv file
    return render_template('favorites.html')


@app.route('/data', methods=['GET', 'POST'])
def data():
    # Data page to show what the data looks like
    df = pd.read_csv('data/final_html.csv')
    df.drop('Unnamed: 0', axis =1, inplace=True)
    df.fillna(0, inplace=True)
    list_of_vals = [list(df[i].values) for i in df]
    columns = df.columns
    return render_template('data.html', data=zip(*list_of_vals), columns=columns)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

