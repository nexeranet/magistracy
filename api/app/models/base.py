from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

times = [ 'M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1' ]	



class main_int(object):

    def create_all_tables(self):
        table_dict = {}
        for cc in crypto_currencies:
            for t in times:
                name = '{}_{}'.format(cc, t)
                table_dict[name] = self.table_creator(name)
        return table_dict

    def table_creator(self,table_name): 
        class Coin_tb(db.Model):
            __tablename__ = table_name
            id = db.Column(db.Integer, primary_key=True, autoincrement=True)
            username = db.Column(db.String(128), nullable=False)
            email = db.Column(db.String(128), nullable=False)
            active = db.Column(db.Boolean(), default=False, nullable=False)
            created_at = db.Column(db.DateTime, nullable=False)

            def __init__(self, username, email):
                self.username = username
                self.email = email
                self.created_at = datetime.now()

            def __repr__(self):
                return '<User %r>' % self.username

        return Coin_tb
        
