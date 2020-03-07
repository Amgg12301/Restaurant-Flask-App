import json
import requests

from flask import Flask, redirect, url_for, request, render_template
from fusionapi import query_api

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("geolocation.html")

@app.route('/results', methods=['GET','POST'])
def results():
    if request.method == 'POST':
        type = request.form['type']
        price = request.form['price']
        location = request.form['yourLocation']
        results = query_api(term = type, location = location);
    return render_template('results.html', results = results)

if __name__ == '__main__':
   app.run(debug = False, port = 0)
