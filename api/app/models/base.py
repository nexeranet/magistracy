from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.sql import text
from datetime import datetime
import time

db = SQLAlchemy()

crypto_currencies = [
        'BTC',
        'ETH',
        'XRP',
        'BCH',
        'ADA',
        'XLM',
        'LTC',
        'NEO',
        'EOS',
        'XEM',
        'IOT',
        'DASH',
        'XMR',
        'TRX',
        'VEN',
        'ETC',
        'ICX',
        'QTUM',
        'OMG',
        'ZEC',
        'LSK',
        'ZIL',
        'ONT',
        'XVG',
        'XRB',
        'STEEM',
        'ZRX',
        'WAVES',
        'SC',
        'DOGE',
        'IOST',
        'DGD'
]

times = ['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1']


class main_int(object):

    def __init__(self):
        self.crypto_currencies = crypto_currencies
        self.times = times

    def create_all_tables(self):
        table_dict = {}
        for cc in crypto_currencies:
            for t in times:
                name = '{}_{}'.format(cc, t)
                table_dict[name] = self.table_creator(name)
        return table_dict

    def table_creator(self, table_name):
        class Coin_tb(db.Model):
            __table_args__ = {'extend_existing': True}
            __tablename__ = table_name
            for_time =     db.Column(db.Integer, nullable=False)
            writing_time = db.Column(db.Integer, nullable=False, primary_key=True)
            c_open =       db.Column(db.DECIMAL(15, 4), nullable=True)
            high =         db.Column(db.DECIMAL(15, 4), nullable=True)
            low =          db.Column(db.DECIMAL(15, 4), nullable=True)
            close =        db.Column(db.DECIMAL(15, 4), nullable=True)

            def __init__(self, for_time, c_open, high, low, close):
                self.writing_time = int(time.time())
                self.for_time = for_time
                self.c_open = c_open
                self.high = high
                self.low = low
                self.close = close

            def __repr__(self):
                return '<Coin table: %r>' % table_name 

        return Coin_tb

    def get_last_updating_time_by_minutes(self, cc, interval): 
        table = self.table_creator('{}_M{}'.format(cc, interval))
        q = db.session.query(func.max(table.writing_time).label('average')).scalar() 

        return q if q is not None else 0

    def add_by_minutes_info(self, cc, interval, data): 
        index = 30 - interval
        high = data[30]['high']
        low = data[30]['low']
        for i in range(index, interval + 1, 1):
            if data[i]['high'] > high:
                high = data[i]['high']
            if data[i]['low'] < low:
                low = data[i]['low']

        table = self.table_creator('{}_M{}'.format(cc, interval))

        coin = table(data[index]['time'], data[index]['open'], high, low, data[30]['close'])

        db.session.add(coin)
        db.session.commit()

    def get_last_updating_time_by_hours(self, cc, interval):

        table = self.table_creator('{}_H{}'.format(cc, interval))
        q = db.session.query(func.max(table.writing_time).label('average')).scalar()
        return q if q is not None else 0

    def add_info_by_hours(self, cc, interval, data):
        index = 4 - interval
        high = data[4]['high']
        low = data[4]['low']
        for i in range(index, interval + 1, 1):
            if data[i]['high'] > high:
                high = data[i]['high']
            if data[i]['low'] < low:
                low = data[i]['low']

        table = self.table_creator('{}_H{}'.format(cc, interval))

        coin = table(data[index]['time'], data[index]['open'], high, low, data[4]['close'])

        db.session.add(coin)
        db.session.commit()

    def add_by_day_info(self, cc, data):
        table = self.table_creator('{}_D1'.format(cc))
        coin = table(data[1]['time'], data[1]['open'], data[1]['high'], data[1]['low'], data[1]['close'])
        db.session.add(coin)
        db.session.commit()

    def get_last_candles(self, cc, period, number_of_candles):
        query = text("SELECT * FROM \"{}_{}\" ORDER BY writing_time DESC LIMIT {} OFFSET 1".format(cc, period, number_of_candles))
        result = db.engine.execute(query)
        rows = result.fetchall()
        return rows
