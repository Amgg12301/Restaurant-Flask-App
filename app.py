import json
import requests

from flask import Flask, redirect, url_for, request, render_template
from fusionapi import query_api

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/results', methods=['GET','POST'])
def results():
    if request.method == 'POST':
        type = request.form['type']
        location = request.form['location']
        price = request.form['price']
        if(price == '$'):
            number_price = 1
        elif(price == '$$'):
            number_price = 2
        elif(price == '$$$'):
            number_price = 3
        else:
            number_price = 4
        x = location.split(", ")
        results = query_api(term = type, latitude = x[0], longitude = x[1], price = number_price);
        if not results:
            results = []
        return render_template('results.html', results = results, price = price)
    else:
        return render_template('geolocation.html')

if __name__ == '__main__':
   app.run(host = 'localhost', debug = True, port = 5000)
