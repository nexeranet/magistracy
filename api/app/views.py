from app import app
from flask import jsonify, render_template
import json
import requests
## https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=30

@app.route("/")
def index():
    url =  'https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=30'
    res = requests.get(url)
    data = res.json()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return render_template('preview.html', data=json.dumps(data))
