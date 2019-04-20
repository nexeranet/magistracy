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
    print(POSTGRES)
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:secret@dbp:5432/coins' 
    print(SQLALCHEMY_DATABASE_URI)
    SECRET_KEY = 'oleh95top95top'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
