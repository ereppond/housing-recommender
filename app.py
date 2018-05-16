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

UPLOAD_FOLDER = 'data/'
ALLOWED_EXTENSIONS = set(['csv'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html') 

@app.route('/uploadajax', methods=['POST'])
def uploadajax():
    file = request.files['file']
    filename=file.filename
    f = BytesIO()
    file.save(f)
    print(f)
    # df = do_everything(f)  # returns pandas df with table to display 
    # list_of_vals = [list(df[i].values) for i in df]
    # columns = df.columns
    # return render_template('uploaded_file.html', data=zip(*list_of_vals), columns=columns)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
#            filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file'))
        else:
            return render_template('index.html')
    return render_template('index.html')


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
    df = pd.read_csv('data/data-for-html-1.csv')
    df.drop('Unnamed: 0', axis =1, inplace=True)
    df.fillna(0, inplace=True)
    list_of_vals = [list(df[i].values) for i in df]
    columns = df.columns
    return render_template('data.html', data=zip(*list_of_vals), columns=columns)
    


def main():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()