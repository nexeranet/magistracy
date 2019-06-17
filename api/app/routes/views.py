from flask import render_template, Blueprint
from app.services.bot import bot

telebot = bot('routes/views')

views = Blueprint('views', __name__, template_folder='templates')


@views.route("/")
def index():
    return render_template('main.html')

# TODO create webhook to telegram bot
@views.route('/webhook', methods=['POST'])
def webhook():
    return 'webhook'


@views.route('/bot')
def bot():
    data = 'hello , Oleg :)'
    r = telebot.sendMessage(data)
    return 'true' if r is True else 'false'
