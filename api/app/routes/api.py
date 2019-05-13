# $route['apiquotes/(:any)'] = 'user/apiquotes/$1';
# $route['apiquotes'] = 'user/apiquotes';
# $route['get_tahometer/(:any)/(:any)'] = 'user/get_tahometer/$1/$2';
# $route['api_correlations/(:any)/(:num)'] = 'user/api_correlations/$1/$2';
# $route['api_correlations'] = 'user/api_correlations';

from flask import jsonify, render_template, Blueprint, redirect
import json ,requests
from app.services.bot import bot 
from app.models.base import main_int
from app.services.mat_helper import math_helper
from app.settings.api import api_config 
from app.settings.json_str import json_str


telebot = bot('routes/api')

api = Blueprint('api', __name__, template_folder='templates' )

apidb = main_int()


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@api.route("/old/quotes/<time>")
def index(time='M5'):
    headers = {"Accept": "*/*", "Connection": "Keep-Alive", "User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.7.12)     Gecko/20050915 Firefox/1.0.7"}
    r = requests.get('http://crypto-quotes.tsianalytics.com/apiquotes/{}'.format(time), headers=headers)    
    data = r.json() 
    return jsonify(data) 

@api.route("/quotes/")
def q_default():
    return redirect('M5', code=302) 

@api.route("/quotes/<period>")
def quotes(period='M5'):

    data = json_str['str_data']
    data['data']['crypto_currencies'] = []
    for cc  in api_config.crypto_currencies:
        currency = {}
        currency['name'] = cc 
        data['data']['crypto_currencies'].append(currency)
    
    lwma_periods = [14, 55, 120, 240]

    for cc in data['data']['crypto_currencies']:
        # //LWMA по 4-м периодам:
        cc['lwmas'] = math_helper.LWMA_calc(cc['name'],period, lwma_periods)
        cc['sell_scores'] = 0
        cc['buy_scores'] = 0

        lwmas_option = ['MA14','MA55','MA120','MA240']; 

        for i in range(0,4,1):
            if not cc['lwmas'][i] == None:
                if cc['lwmas'][i]['last_candle'] <= cc['lwmas'][i]['val']: 
                    cc['sell_scores'] += api_config.tahometer_scores[lwmas_option[i]]
                elif cc['lwmas'][i]['last_candle'] > cc['lwmas'][i]['val']: 
                    cc['buy_scores'] += api_config.tahometer_scores[lwmas_option[i]]

        # BB:
        cc['bb'] = math_helper.BB_calc(cc['name'], period)       

        if not cc['bb']['up'] == None and cc['bb']['up'] <= cc['bb']['last_candle']:
           cc['sell_scores'] += api_config.tahometer_scores['BB'] 
        elif not cc['bb']['down'] == None and cc['bb']['down'] >= cc['bb']['last_candle']:
           cc['buy_scores'] += api_config.tahometer_scores['BB'] 

        # ATR:
        cc['atr'] = math_helper.ATR_calc(cc['name'],period)
        # DC:
        cc['dc'] = math_helper.DC_calc(cc['name'], period)
        if not cc['dc']['up'] == None and cc['dc']['up'] < cc['dc']['last_candle']:
           cc['buy_scores'] += api_config.tahometer_scores['DC'] 
        elif not cc['dc']['down'] == None and cc['dc']['down'] > cc['dc']['last_candle']:
           cc['sell_scores'] += api_config.tahometer_scores['DC'] 
        # RSI(0-100)
        cc['rsi'] = math_helper.RSI_calc(cc['name'], period)
    
        if not cc['rsi'] == None and cc['rsi'] > 70:
           cc['sell_scores'] += api_config.tahometer_scores['RSI'] 
        elif not cc['rsi'] == None and cc['rci'] < 30:
           cc['buy_scores'] += api_config.tahometer_scores['RSI'] 
         # BBP
        cc['bbp'] = math_helper.BBP_calc(cc['name'], period)

        if not cc['bbp'] == None and cc['bbp'] >= 0:
           cc['buy_scores'] += api_config.tahometer_scores['BBP'] 
        elif not cc['bbp'] == None and cc['bbp'] < 0:
           cc['sell_scores'] += api_config.tahometer_scores['BBP'] 
        
        # MACD
        macds_corteg = math_helper.MACD_calc(cc['name'], period)
        cc['signal'] = macds_corteg['signal']
        cc['macd'] = macds_corteg['macd']
        if not cc['signal'] == None and not cc['macd'] == None:
            if cc['signal'] >= 0 and cc['macd'] >= 0:
                cc['buy_scores'] += api_config.tahometer_scores['MACD']
            elif cc['macd'] < 0 and cc['signal'] < 0:
                cc['sell_scores'] += api_config.tahometer_scores['MACD']

        # AO 
        cc['ao'] = math_helper.AO_calc(cc['name'], period)
        if not cc['ao']['f'] == None and not cc['ao']['s'] == None:
            if cc['ao']['f'] > cc['ao']['s'] and cc['ao']['f'] >= 0 and cc['ao']['s'] >= 0:
                cc['buy_scores'] += api_config.tahometer_scores['AO']
            elif cc['ao']['f'] < cc['ao']['s'] and cc['ao']['f'] < 0 and cc['ao']['s'] < 0:
                cc['sell_scores'] += api_config.tahometer_scores['AO']

        #// ADX:

        cc['adx'] = math_helper.ADX_calc(cc['name'], period)

        #// SO:
        cc['so'] = math_helper.SO_calc(cc['name'], period)
        if not cc['so'] == None:
            if cc['so'] >= 80:
                cc['sell_scores'] += api_config.tahometer_scores['SO']
            elif cc['so'] <= 20:
                cc['buy_scores'] += api_config.tahometer_scores['SO']
        
        scores_sum = 0 if cc['sell_scores'] == cc['buy_scores'] else cc['sell_scores'] + cc['buy_scores']
        cc['sell_percent'] = 0 if scores_sum == 0 else (cc['sell_scores']*100)/scores_sum
        cc['buy_percent'] = 0 if scores_sum == 0 else (cc['buy_scores']*100)/scores_sum 
        cc['tahometer_percent'] = 50 if scores_sum == 0 else (cc['buy_scores']*100)/scores_sum 

    return jsonify(data) 

