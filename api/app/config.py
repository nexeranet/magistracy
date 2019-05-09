# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:secret@dbp:5432/coins' 

import os
class config(object):
    DEBAG = True
    POSTGRES = {
        'user': os.environ.get('POSTGRES_USER'),
        'pw': os.environ.get('POSTGRES_PASSWORD'),
        'db': os.environ.get('POSTGRES_DB'),
        'host': os.environ.get('POSTGRES_HOSTDOCKER'),
        'port': os.environ.get('POSTGRES_PORT'),
        }
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SECRET_KEY = 'oleh95top95top'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
