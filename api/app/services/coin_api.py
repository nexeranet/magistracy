## https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=30
import requests
from app.services.bot import bot

tbot = bot('services/coin_api')

class coin_api(object):

    def get_api(self,url): 
        # return json
        # headers = defaults 
        try:
            r = requests.get(url)
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            error = {'errorType': 'Timeout', 'url': url}
            tbot.sendMessage(error)
            return False 
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            error = {'errorType': 'TooManyRedirects', 'url': url}
            tbot.sendMessage(error)
            return False
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            error = {'errorType': 'RequestException', 'url': url, 'error': e}
            tbot.sendMessage(error)
            return False
        data = r.json()
        if data['Response'] == 'Success':
            return data
        else:
            error = {'url':url,'data': data}
            tbot.sendMessage(error)
            return False
 
    def get_minutes(self, cc):
        # return json
        return self.get_api('https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym=USD&limit=30'.format(cc))

    def get_hours(self, cc):
        # return json
        return self.get_api('https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym=USD&limit=4'.format(cc))

    def get_day(self, cc):
        # return json
        return self.get_api('https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym=USD&limit=1'.format(cc));

