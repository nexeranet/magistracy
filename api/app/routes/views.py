from flask import jsonify, render_template, Blueprint
import json
import requests
from app.models.base import User, db
## https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=30

views = Blueprint('views', __name__, template_folder='templates' )

@views.route("/")
def index():
    url =  'https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=30'
    res = requests.get(url)
    data = res.json()
    
    return render_template('preview.html', data=json.dumps(data))
@views.route('/db')
def db_add():
    db.create_all()
    client = User(username='oleh',email='oleh@mail.com')
    db.session.add(client)
    db.session.commit()
    try:
        return 'true'
    except:
        return 'Error'

    return "database is True"
