import json
import requests

from flask import Flask, redirect, url_for, request, render_template
from fusionapi import query_api

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        type = request.form['type']
        location = request.form['location']
        price = request.form['price']
        number = request.form['number']
        transactions = []

        if number > 50:
            number = 50
        elif number == 0:
            number = 10

        if price == '$':
            number_price = 1
        elif price == '$$':
            number_price = 2
        elif price == '$$$':
            number_price = 3
        else:
            number_price = 4

        x = location.split(", ")
        latitude = x[0]
        longitude = x[1]
        results = query_api(term=type, latitude=latitude, longitude=longitude, price=number_price, number=number)

        if not results:
            results = []

        for business in results:
            print(business['transactions'])
            if 'delivery' in business['transactions'] and 'pickup' in business['transactions']:
                transactions.append("Delivery and Pickup are both available!")
            elif 'pickup' in business['transactions']:
                transactions.append("Only pickup is available!")
            elif 'delivery' in business['transactions']:
                transactions.append("Only delivery is available!")
            else:
                transactions.append("Both options are unavailable, sorry :(")
            print(transactions)

        return render_template('results.html', transactions=transactions, results=results,
                               results_and_transactions=zip(results, transactions), price=price,
                               latitude=latitude, longitude=longitude)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=0)
