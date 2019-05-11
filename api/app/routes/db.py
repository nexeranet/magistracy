## https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=30
# $route['create_tables_once'] = 'apic/create_tables_once';
# $route['alter_tables'] = 'apic/alter_tables';
# $route['drop_tables'] = 'apic/drop_tables';
# $route['add_info_by_minutes'] = 'apic/add_info_by_minutes';
# $route['add_info_by_hours'] = 'apic/add_info_by_hours';
# $route['add_info_by_day'] = 'apic/add_info_by_day';

from flask import jsonify, Blueprint
import json, requests, time
from datetime import datetime

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
    try:
        db.create_all()
        db.session.commit() 
    except:
        tbot.sendMessage('Error. Table not create');
        return 'Error' 

    return 'table create'

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
    now = int(time.time())
    ## loop coins 
    for cc in tr_db.crypto_currencies: 

        data = crypto.get_minutes(cc) 

        tr_db.add_by_minutes_info(cc=cc, interval=1, data=data['Data'])
        tr_db.add_by_minutes_info(cc=cc, interval=5, data=data['Data'])

        #  60 * N , N - 15 || 30

        lm15 = tr_db.get_last_updating_time_by_minutes(cc=cc,interval=15)
        if (now - lm15) >= 900 or lm15 == 0: 
            tr_db.add_by_minutes_info(cc=cc, interval=15, data=data['Data'])

        lm30 = tr_db.get_last_updating_time_by_minutes(cc=cc,interval=30)

        if (now - lm30) >= 1800 or lm30 == 0: 
            tr_db.add_by_minutes_info(cc=cc, interval=30, data=data['Data'])

    tbot.sendMessage('Parse minutes for coins: {}'.format(tr_db.crypto_currencies))
    return 'by_minutes'

@apidb.route('add_info_by_hours')
def by_hours():
    now = int(time.time())

    for cc in tr_db.crypto_currencies: 
        data = crypto.get_hours(cc) 
        print('hell')
    tbot.sendMessage('Parse hours for coins: {}'.format(tr_db.crypto_currencies))
    return 'by_hours'

@apidb.route('add_info_by_day')
def by_day():
    return 'by_day'


