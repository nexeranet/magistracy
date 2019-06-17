
from flask import jsonify, render_template, Blueprint, redirect
import json
import requests
from app.services.bot import bot
from app.models.base import main_int
from app.services.mat_helper import math_helper
from app.settings.api import api_config
from app.settings.json_str import json_str


telebot = bot('routes/api')

api = Blueprint('api', __name__, template_folder='templates')

apidb = main_int()


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

#
# OLD API ROUTES
#


@api.route("/old/quotes/<time>")
def old_quotes(time='M5'):
    time = time.upper()
    if time in api_config.times:
        headers = {
            "Accept": "*/*",
            "Connection": "Keep-Alive",
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7"}
        r = requests.get('http://crypto-quotes.tsianalytics.com/apiquotes/{}'.format(time), headers=headers)
        data = r.json()
        return jsonify(data)
    else:
        data = json_str['std_error']
        data['message'] = 'error. invalid timeframe'
        return jsonify(data)


@api.route("/old/correlations/<time>/<int:num>")
def old_correlations(time='M15', num=15):
    time = time.upper()
    if time not in api_config.correlations_times or num not in api_config.correlations_periods:
        print(time, num)
        data = json_str['std_error']
        data['message'] = 'error. invalid params'
        return jsonify(data)
    else:
        headers = {
            "Accept": "*/*",
            "Connection": "Keep-Alive",
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7"}
        r = requests.get('http://crypto-quotes.tsianalytics.com/api_correlations/{}/{}'.format(time, num), headers=headers)
        data = r.json()
        return jsonify(data)


@api.route("/old/get_tahometer/<coin>/<time>")
def old_get_tahometer(coin="BTC", time='M5'):
    if time not in api_config.times or coin not in api_config.crypto_currencies:
        data = json_str['std_error']
        data['message'] = 'error. invalid params'
        return jsonify(data)
    else:
        headers = {
            "Accept": "*/*",
            "Connection": "Keep-Alive",
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7"}
        r = requests.get('http://crypto-quotes.tsianalytics.com/get_tahometer/{}/{}'.format(coin, time), headers=headers)
        res = r.json()
        data = json_str['std_data']
        data['data'] = str(res)
        return jsonify(data)


#
# MAIN API ROUTES
#

@api.route("/quotes/")
def q_default():
    return redirect('M15', code=302)


@api.route("/quotes/<period>", methods=['GET', 'POST'])
def quotes(period='M5'):
    period = period.upper()
    if period not in api_config.times:
        data = json_str['std_error']
        data['message'] = 'Error. Invalid timeframe'
        return jsonify(data)

    data = {
        "status" : "success",
        "data" : {}
    }
    data['data']['crypto_currencies'] = []
    for cc in api_config.crypto_currencies:
        currency = {}
        currency['name'] = cc
        data['data']['crypto_currencies'].append(currency)

    lwma_periods = [14, 55, 120, 240]

    for cc in data['data']['crypto_currencies']:
        # //LWMA по 4-м периодам:
        cc['lwmas'] = math_helper.LWMA_calc(cc['name'], period, lwma_periods)
        cc['sell_scores'] = 0
        cc['buy_scores'] = 0

        lwmas_option = ['MA14', 'MA55', 'MA120', 'MA240']

        for i in range(0, 4, 1):
            if cc['lwmas'][i] is not None:
                if cc['lwmas'][i]['last_candle'] <= cc['lwmas'][i]['val']:
                    cc['sell_scores'] += api_config.tahometer_scores[lwmas_option[i]]
                elif cc['lwmas'][i]['last_candle'] > cc['lwmas'][i]['val']:
                    cc['buy_scores'] += api_config.tahometer_scores[lwmas_option[i]]

        # BB:
        cc['bb'] = math_helper.BB_calc(cc['name'], period)

        if cc['bb']['up'] is not None and cc['bb']['up'] <= cc['bb']['last_candle']:
            cc['sell_scores'] += api_config.tahometer_scores['BB']
        elif cc['bb']['down'] is not None and cc['bb']['down'] >= cc['bb']['last_candle']:
            cc['buy_scores'] += api_config.tahometer_scores['BB']

        # ATR:
        cc['atr'] = math_helper.ATR_calc(cc['name'], period)
        # DC:
        cc['dc'] = math_helper.DC_calc(cc['name'], period)
        if cc['dc']['up'] is not None and cc['dc']['up'] < cc['dc']['last_candle']:
            cc['buy_scores'] += api_config.tahometer_scores['DC']
        elif cc['dc']['down'] is not None and cc['dc']['down'] > cc['dc']['last_candle']:
            cc['sell_scores'] += api_config.tahometer_scores['DC']
        # RSI(0-100)
        cc['rsi'] = math_helper.RSI_calc(cc['name'], period)

        if cc['rsi'] is not None and cc['rsi'] > 70:
            cc['sell_scores'] += api_config.tahometer_scores['RSI']
        elif cc['rsi'] is not None and cc['rsi'] < 30:
            cc['buy_scores'] += api_config.tahometer_scores['RSI']
        # BBP
        cc['bbp'] = math_helper.BBP_calc(cc['name'], period)

        if cc['bbp'] is not None and cc['bbp'] >= 0:
            cc['buy_scores'] += api_config.tahometer_scores['BBP']
        elif cc['bbp'] is not None and cc['bbp'] < 0:
            cc['sell_scores'] += api_config.tahometer_scores['BBP']

        # MACD
        macds_corteg = math_helper.MACD_calc(cc['name'], period)
        cc['signal'] = macds_corteg['signal']
        cc['macd'] = macds_corteg['macd']
        if cc['signal'] is not None and cc['macd'] is not None:
            if cc['signal'] >= 0 and cc['macd'] >= 0:
                cc['buy_scores'] += api_config.tahometer_scores['MACD']
            elif cc['macd'] < 0 and cc['signal'] < 0:
                cc['sell_scores'] += api_config.tahometer_scores['MACD']

        # AO
        cc['ao'] = math_helper.AO_calc(cc['name'], period)
        if cc['ao']['f'] is not None and cc['ao']['s'] is not None:
            if cc['ao']['f'] > cc['ao']['s'] and cc['ao']['f'] >= 0 and cc['ao']['s'] >= 0:
                cc['buy_scores'] += api_config.tahometer_scores['AO']
            elif cc['ao']['f'] < cc['ao']['s'] and cc['ao']['f'] < 0 and cc['ao']['s'] < 0:
                cc['sell_scores'] += api_config.tahometer_scores['AO']

        # // ADX:

        cc['adx'] = math_helper.ADX_calc(cc['name'], period)

        # // SO:
        cc['so'] = math_helper.SO_calc(cc['name'], period)
        if cc['so'] is not None:
            if cc['so'] >= 80:
                cc['sell_scores'] += api_config.tahometer_scores['SO']
            elif cc['so'] <= 20:
                cc['buy_scores'] += api_config.tahometer_scores['SO']

        scores_sum = 0 if cc['sell_scores'] == cc['buy_scores'] else cc['sell_scores'] + cc['buy_scores']
        cc['sell_percent'] = 0 if scores_sum == 0 else (cc['sell_scores']*100)/scores_sum
        cc['buy_percent'] = 0 if scores_sum == 0 else (cc['buy_scores']*100)/scores_sum
        cc['tahometer_percent'] = 50 if scores_sum == 0 else (cc['buy_scores']*100)/scores_sum
    response = jsonify(data) 
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@api.route('/quote/<coin>/<period>', methods=['GET', 'POST'])
def quote(coin="BTC", period='M5'):

    if period not in api_config.times or coin not in api_config.crypto_currencies:
        data = json_str['std_error']
        data['message'] = 'error. invalid params'
        return jsonify(data)

    data = {
        "status" : "success",
        "data" : {}
    }
    lwma_periods = [14, 55, 120, 240]
    cc = {}
    cc['name'] = coin
    # //LWMA по 4-м периодам:
    cc['lwmas'] = math_helper.LWMA_calc(cc['name'], period, lwma_periods)
    cc['sell_scores'] = 0
    cc['buy_scores'] = 0

    lwmas_option = ['MA14', 'MA55', 'MA120', 'MA240']

    for i in range(0, 4, 1):
        if cc['lwmas'][i] is not None:
            if cc['lwmas'][i]['last_candle'] <= cc['lwmas'][i]['val']:
                cc['sell_scores'] += api_config.tahometer_scores[lwmas_option[i]]
            elif cc['lwmas'][i]['last_candle'] > cc['lwmas'][i]['val']:
                cc['buy_scores'] += api_config.tahometer_scores[lwmas_option[i]]

    # BB:
    cc['bb'] = math_helper.BB_calc(cc['name'], period)

    if cc['bb']['up'] is not None and cc['bb']['up'] <= cc['bb']['last_candle']:
        cc['sell_scores'] += api_config.tahometer_scores['BB']
    elif cc['bb']['down'] is not None and cc['bb']['down'] >= cc['bb']['last_candle']:
        cc['buy_scores'] += api_config.tahometer_scores['BB']

    # ATR:
    cc['atr'] = math_helper.ATR_calc(cc['name'], period)
    # DC:
    cc['dc'] = math_helper.DC_calc(cc['name'], period)
    if cc['dc']['up'] is not None and cc['dc']['up'] < cc['dc']['last_candle']:
        cc['buy_scores'] += api_config.tahometer_scores['DC']
    elif cc['dc']['down'] is not None and cc['dc']['down'] > cc['dc']['last_candle']:
        cc['sell_scores'] += api_config.tahometer_scores['DC']
    # RSI(0-100)
    cc['rsi'] = math_helper.RSI_calc(cc['name'], period)

    if cc['rsi'] is not None and cc['rsi'] > 70:
        cc['sell_scores'] += api_config.tahometer_scores['RSI']
    elif cc['rsi'] is not None and cc['rsi'] < 30:
        cc['buy_scores'] += api_config.tahometer_scores['RSI']
    # BBP
    cc['bbp'] = math_helper.BBP_calc(cc['name'], period)

    if cc['bbp'] is not None and cc['bbp'] >= 0:
        cc['buy_scores'] += api_config.tahometer_scores['BBP']
    elif cc['bbp'] is not None and cc['bbp'] < 0:
        cc['sell_scores'] += api_config.tahometer_scores['BBP']

    # MACD
    macds_corteg = math_helper.MACD_calc(cc['name'], period)
    cc['signal'] = macds_corteg['signal']
    cc['macd'] = macds_corteg['macd']
    if cc['signal'] is not None and cc['macd'] is not None:
        if cc['signal'] >= 0 and cc['macd'] >= 0:
            cc['buy_scores'] += api_config.tahometer_scores['MACD']
        elif cc['macd'] < 0 and cc['signal'] < 0:
            cc['sell_scores'] += api_config.tahometer_scores['MACD']

    # AO
    cc['ao'] = math_helper.AO_calc(cc['name'], period)
    if cc['ao']['f'] is not None and cc['ao']['s'] is not None:
        if cc['ao']['f'] > cc['ao']['s'] and cc['ao']['f'] >= 0 and cc['ao']['s'] >= 0:
            cc['buy_scores'] += api_config.tahometer_scores['AO']
        elif cc['ao']['f'] < cc['ao']['s'] and cc['ao']['f'] < 0 and cc['ao']['s'] < 0:
            cc['sell_scores'] += api_config.tahometer_scores['AO']

    # // ADX:

    cc['adx'] = math_helper.ADX_calc(cc['name'], period)

    # // SO:
    cc['so'] = math_helper.SO_calc(cc['name'], period)
    if cc['so'] is not None:
        if cc['so'] >= 80:
            cc['sell_scores'] += api_config.tahometer_scores['SO']
        elif cc['so'] <= 20:
            cc['buy_scores'] += api_config.tahometer_scores['SO']

    scores_sum = 0 if cc['sell_scores'] == cc['buy_scores'] else cc['sell_scores'] + cc['buy_scores']
    cc['sell_percent'] = 0 if scores_sum == 0 else (cc['sell_scores']*100)/scores_sum
    cc['buy_percent'] = 0 if scores_sum == 0 else (cc['buy_scores']*100)/scores_sum
    cc['tahometer_percent'] = 50 if scores_sum == 0 else (cc['buy_scores']*100)/scores_sum

    data['data']['coin'] = cc

    response = jsonify(data) 
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@api.route('/correlations/<time>/<int:num>', methods=['GET', 'POST'])
def correlations(time='M15', num=15):
    time = time.upper()
    if time not in api_config.correlations_times or num not in api_config.correlations_periods:
        data = {
            "status" : "success",
            "data" : {}
        }
        data['message'] = 'error. invalid params'
        return jsonify(data)

    data = json_str['std_data']
    data['data']['crypto_currencies'] = []
    for cc in api_config.crypto_currencies:
        currency = {}
        currency['name'] = cc
        data['data']['crypto_currencies'].append(currency)
    data['data']['current_timeframe'] = time
    data['data']['current_period'] = num
    data['data']['timeframes'] = api_config.correlations_times
    data['data']['periods'] = api_config.correlations_periods
    close_candles = {}

    for cc in api_config.crypto_currencies:
        close_candles[cc] = apidb.get_last_candles(cc, time, num)
        cc_arr = []
        for val in close_candles[cc]:
            cc_arr.append(val.close)
        close_candles[cc] = cc_arr

    correlation_matrix = []
    i = 0
    j = 0
    for cc_i in api_config.crypto_currencies:
        row = []
        for cc_j in api_config.crypto_currencies:
            result = math_helper.get_correlation(close_candles[cc_i], close_candles[cc_j])
            row.append(round(result, 10))
            j += 1
        correlation_matrix.append(row)
        i += 1
        j = 0

    data['data']['correlation_matrix'] = correlation_matrix
    response = jsonify(data) 
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
