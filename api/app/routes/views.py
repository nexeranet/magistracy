from flask import jsonify, render_template, Blueprint
import json
import requests
from app.services.bot import bot

telebot = bot('routes/views')

views = Blueprint('views', __name__, template_folder='templates')


@views.route("/")
def index():
    url = 'https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=30'
    try:
        res = requests.get(url)
    except requests.exceptions.ConnectionError:
        return 'error'
    data = res.json()
    return render_template('preview.html', data=json.dumps(data))

# TODO create webhook to telegram bot
@views.route('/webhook', methods=['POST'])
def webhook():
    return 'webhook'


@views.route('/bot')
def bot():
    data = 'hello , Oleg :)'
    r = telebot.sendMessage(data)
    return 'true' if r is True else 'false'
