"""
Simple flask app.
"""
from flask import (Flask,
                   jsonify,
                   render_template,
                   request, 
                   url_for)
import tablib
import os
import pandas as pd
# from ec2.prophet_db import web_query

app = Flask(__name__)
dataset = tablib.Dataset()
with open(os.path.join(os.path.dirname(__file__),'data/data-for-html-1.csv')) as f:
    dataset.csv = f.read()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
#    if request.method == 'GET':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
#        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('welcome.html')


@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
#    if request.method == 'GET':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
#        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('favorites.html')


@app.route('/data', methods=['GET', 'POST'])
def data():
    data = dataset.html
    return render_template('data.html', data=data)
    


def main():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()