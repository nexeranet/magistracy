## https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=30
# $route['create_tables_once'] = 'apic/create_tables_once';
# $route['alter_tables'] = 'apic/alter_tables';
# $route['drop_tables'] = 'apic/drop_tables';
# $route['add_info_by_minutes'] = 'apic/add_info_by_minutes';
# $route['add_info_by_hours'] = 'apic/add_info_by_hours';
# $route['add_info_by_day'] = 'apic/add_info_by_day';

from flask import jsonify, Blueprint
import json, requests
from app.services.bot import bot 
from app.models.base import db, main_int  
from app.services.coin_api import coin_api

tbot = bot('routes/db')

crypto = coin_api()

tr_db = main_int()

apidb = Blueprint('apidb', __name__, template_folder='templates' )

@apidb.route("/")
def index():
    r = crypto.get_minutes('BTC');
    #r = tbot.sendMessagedata;
    return jsonify(r)

@apidb.route('/create_all')
def craate_all():
    tr_db.create_all_tables()
    # client = User(username='oleh',email='oleh@mail.com')
    # db.session.add(client)
    # db.session.commit()
    try:
        db.create_all()
    except:
        return 'Error' 

    return 'table craate_all'

@apidb.route('alter_tables')
def alter_tables():
    return 'alter'

@apidb.route('drop_tables')
def drop_tables():
    db.session.commit()   #<--- solution!
    db.drop_all()
    return 'drop'

@apidb.route('add_info_by_minutes')
def by_minutes():
    return 'by_minutes'

@apidb.route('add_info_by_hours')
def by_hours():
    return 'by_hours'

@apidb.route('add_info_by_day')
def by_day():
    return 'by_day'


