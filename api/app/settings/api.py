class Api_Config(object):
    def __init__(self):
        self.crypto_currencies = [
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
				'TRX' ]
        self.times = [ 'M5', 'H1', 'H4', 'D1'] 
        self.tahometer_scores = {
                'MA14' : 1, 
                'MA55' :2, 
                'MA120' :3,
                'MA240' :4,
                'BB' :3,   # N/S - 0 
                'DC' :2,   # N/S - 0
                'BBP' :2,
                'RSI' :2,  # Neutral - 0 
                'MACD': 3, # Neutral - 0
                'SO' :2,   # Neutral - 0
                'AO' :3    # Neutral - 0
                }
        self.correlations_times = [ 'M15', 'M30', 'H1', 'H4', 'D1' ] 
        self.correlations_periods = [ 7, 14, 30 ] # full list - 7 , 14, 15, 45, 90

api_config = Api_Config()
