import json
import requests

from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

api_key = 'Ah-aLz_0uR4JkXM3jQIGuGb5ci5c79cQrFfsRGGOia_UZBjBmuLNGplv_1eg5LGUS-AyKYcLN_dW9LUj99y-7sChsTMsC0iL2941i6JlSZo25CciOmDYFA8AGoVPXnYx'
headers = {'Authorization': 'Bearer %s' % api_key}

def get_restaurant(restaurant, location):
    url = 'https://api.yelp.com/v3/businesses/search'
    params = {'term': restaurant,'location': location}

    req = requests.get(url, params=params, headers=headers)

    parsed = json.loads(req.text)

    businesses = parsed["businesses"]
    #for business in businesses:
     #   print("Name:", business["name"])
      #  print("Rating:", business["rating"])
       # print("Address:", " ".join(business["location"]["display_address"]))
        #print("Phone:", business["phone"])
        #print("\n")
    return businesses;


@app.route('/results/<type>/<distance>')
def success(type, distance):
    return "So, you want some %s food within %s miles right?" % (type, distance)

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['type']
      loc = request.form['distance']
      return redirect(url_for('success',type = user, distance = loc))
   else:
      user = request.args.get('type')
      loc = request.args.get('distance')
      return redirect(url_for('success',type = user, distance = loc))

if __name__ == '__main__':
   app.run(debug = True, port = 0)
