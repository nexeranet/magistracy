# bot api 

import requests, json 
from datetime import datetime
from flask import jsonify

TOKEN = '745808780:AAEyL5EGVrPWwUPXQpRol5TOYarkH-vF87Q' 
URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)
chat_id = '390306402'

def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_chat_id():
    # u = URL + 'getUpdates'
    # r = requests.get(u)
    # data = r.json()
    print('Bot init')
    # if data['ok'] == True : 
        # chat_id = data['result'][-1]['message']['chat']['id']

get_chat_id()

class bot(object):

    def __init__(self,module):
        self.chat_id = chat_id 
        self.module = module

    def __repr__(self):
        return '<Bot %r>' % URL 

    def getMe(self):    
        r = requests.get(URL + 'getme') 
        data = r.json() 
        write_json(data)
        return jsonify(data)

    def getUpdates(self):
        u = URL + 'getUpdates'
        r = requests.get(u)
        data = r.json()
        write_json(data)
        return jsonify(data)

    def sendMessage(self, text='bla bla'): 
        u = URL + 'sendMessage'

        now = 'Дата: {}'.format(datetime.now()) 
        module = 'Модуль: {}'.format(self.module)
        text = str(text)
        f_txt = (text[:4040] + '..') if len(text) > 4096 else text 

        msg = '<i>{}</i>\n<b>{}</b>\n<code>{}</code>'.format(now, module, f_txt)

        answer = {'chat_id': self.chat_id, 'text':msg,'parse_mode':'HTML'}

        r = requests.post(u, json=answer)
        data = r.json()
        return True if data['ok'] == True else False 
