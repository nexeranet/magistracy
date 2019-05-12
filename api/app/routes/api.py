# $route['quotes/(:any)'] = 'user/quotes/$1';
# $route['quotes'] = 'user/quotes';
# $route['correlations/(:any)/(:num)'] = 'user/correlations/$1/$2';
# $route['correlations'] = 'user/correlations';
# $route['apiquotes/(:any)'] = 'user/apiquotes/$1';
# $route['apiquotes'] = 'user/apiquotes';
# $route['get_tahometer/(:any)/(:any)'] = 'user/get_tahometer/$1/$2';
# $route['api_correlations/(:any)/(:num)'] = 'user/api_correlations/$1/$2';
# $route['api_correlations'] = 'user/api_correlations';
# $route['test'] = 'user/test';

from flask import jsonify, render_template, Blueprint, redirect
import json
import requests
from app.services.bot import bot 
from app.models.base import main_int
telebot = bot('routes/api')

api = Blueprint('api', __name__, template_folder='templates' )

apidb = main_int()

@api.route("/")
def index():

    return 'api main url'

@api.route("/quotes/<time>")
def quotes(time='M5'):
    return time;

@api.route("/quotes/")
def q_default():
    return 'hello!:) this queotes'
