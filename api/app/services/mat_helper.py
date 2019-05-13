# helper for mat. models
import math
from app.models.base import main_int

helperdb = main_int()

class mathHelper(object):

    def fill_ema_array(self, period, candles, emm_arr):

        p = 2 / (period + 1)
        for i in range(period,-1,-1):
            if i == period:
                s = 0 
                for j in range(period + 1, (period * 2) + 1,1):
                    s += candles[j].close
                emm_arr[i] = s / period 
            else:
                emm_arr[i] = (candles[i].close * p ) + emm_arr[i + 1] * (1 - p) 
        return emm_arr


    def adx(self, candles):

        sum_of_dx = 0
        for i in range(27, 13, -1):
            sum_of_dx += self.dx(i, candles)
        return sum_of_dx / 14


    def dx(self, i, candles):
        
        tr_14_i = self.tr_14(i, candles)
        pdi = 0 if tr_14_i == 0 else 100 * (self.positive_dm_14(i,candles) / tr_14_i)
        mdi = 0 if tr_14_i == 0 else 100 * (self.positive_dm_14(i,candles) / tr_14_i)
        return 0 if pdi + mdi == 0 else 100 * (abs(pdi - mdi)/(pdi + mdi))


    def positive_dm_14(self, i, candles):

        if i == 14: 
            sum_of_pdm_1 = 0
            for j in range(1, 15, 1):
                sum_of_pdm_1 += self.positive_dm_1(j, candles)
            return sum_of_pdm_1
        else:
            prev_pdm_14 = self.positive_dm_14(i - 1, candles)
            return prev_pdm_14 - (prev_pdm_14 / 14) + self.positive_dm_1(i, candles)
            

    def negative_dm_14(self, i, candles):

        if i == 14: 
            sum_of_ndm_1 = 0
            for j in range(1, 15, 1):
                sum_of_ndm_1 += self.negative_dm_14(j, candles)
            return sum_of_ndm_1
        else:
            prev_ndm_14 = self.negative_dm_14(i - 1, candles)
            return prev_ndm_14 - (prev_ndm_14 / 14) + self.negative_dm_1(i, candles)
            

    def tr_14(self, i, candles):
        if i == 14: 
            sum_of_tr_1 = 0
            for j in range(1, 15, 1):
                sum_of_tr_1 += self.tr_1(j, candles)
            return sum_of_tr_1
        else:
            prev_tr_14 = self.tr_14(i - 1, candles)
            return prev_tr_14 - (prev_tr_14 / 14) + self.tr_1(i, candles)

    def positive_dm_1(self, i, candles):
        # return $candles[$i]->high - $candles[$i - 1]->high > $candles[$i - 1]->low - $candles[$i]->low ? max($candles[$i]->high - $candles[$i - 1]->high, 0) : 0
        return  max(candles[i].high - candles[i - 1].high, 0) if candles[i].high - candles[i - 1].high > candles[i - 1].low - candles[i].low else 0  


    def negative_dm_1(self, i, candles):
        # return $candles[$i - 1]->low - $candles[$i]->low > $candles[$i]->high - $candles[$i - 1]->high ? max($candles[$i - 1]->low - $candles[$i]->low, 0) : 0;
        return max(candles[i - 1].low - candles[i].low, 0) if candles[i -  1].low - candles[i].low > candles[i].high - candles[i - 1].high else 0  


    def tr_1(self, i, candles):
        # return max($candles[$i]->high - $candles[$i]->low, abs($candles[$i]->high - $candles[$i-1]->close), abs($candles[$i]->low - $candles[$i-1]->close));
        return max(candles[i].high - candles[i].low, abs(candles[i].high - candles[i - 1].close), abs(candles[i].low - candles[i - 1].close)) 

    def get_correlation(self, arr1, arr2): 

        if len(arr1) == 0 or len(arr2) == 0:
            return 100

        min_count = min(len(arr1), len(arr2))
        s1 = 0
        for i in range(0, min_count, 1):
            s1 += arr1[i]
        
        avg_arr1 = 0 if min_count == 0 else s1 / min_count
        
        s2 = 0 

        for i in range(0, min_count, 1):
            s2 += arr2[i]

        avg_arr2 = 0 if min_count == 0 else s2 / min_count 

        numerator = 0 
        for i in range(0, min_count, 1):
            numerator += (arr1[i] - avg_arr1)*(arr2[i] - avg_arr2)

        denominator_part_x = 0
        for i in range(0, min_count, 1):
            denominator_part_x += pow(arr1[i] - avg_arr1, 2)

        denominator_part_y = 0
        for i in range(0, min_count, 1):
            denominator_part_y += pow(arr2[i] - avg_arr2, 2)

        denominator = math.sqrt(denominator_part_x * denominator_part_y)
        return 0 if denominator == 0 else numerator / denominator 

    ## 
    ## mat models for coin
    ##
        
    def LWMA_calc(self, coin, period, lwma_periods):

        lwmas = []
        for lwma_p in lwma_periods:

            candles = helperdb.get_last_candles(coin, period, lwma_p)
            if len(candles) < lwma_p:
                lwmas.append(None) 
            else:
                lwma_numerator_parts = []
                i = 1
                for candle in candles:
                    lwma_numerator_parts.append(abs(i - (lwma_p - 1))*candle.close)
                    i+=1
                weight_sum = 0
                for i in range(1,lwma_p + 1,1):
                    weight_sum += abs(i - lwma_p - 1)
                lwma = {}
                lwma['last_candle'] = candles[0].close
                lwma['val'] = sum(lwma_numerator_parts)/weight_sum
                lwmas.append(lwma)

        return lwmas
        
    def BB_calc(self, coin, period):
        candles = helperdb.get_last_candles(coin, period, 20)
        if len(candles) < 20:
            return {
                    "up": None,
                    "down":None
                    }
        else: 
            closes_sum = 0
            for candle in candles:
                closes_sum += candle.close
            ma = closes_sum/20
            std_sum = 0
            for candle in candles:
                std_sum += (candle.close - ma)**2

            std = math.sqrt(std_sum/19)
            bb_up = ma + 2*std
            bb_down = ma - 2 *std
            bb_last_candle = candles[0].close
            return {
                    "up" : bb_up,
                    "down": bb_down,
                    "last_candle": bb_last_candle
                    }


    def ATR_calc(self, coin, period):
        c = helperdb.get_last_candles(coin, period, 15)
        if len(c) < 15:
            return None
        else:
            tr_sum = 0
            for i in range(1,15,1):
                tr_sum += max(c[i-1].high - c[i-1].low, c[i-1].high - c[i].close, c[i].close - c[i-1].low)
            return tr_sum/14
    
    def DC_calc(self, coin, period):
        candles = helperdb.get_last_candles(coin, period, 15)
     
        if len(candles) < 15:
            return {
                    "up": None,
                    "down":None
                    }
        else: 
            dc_up = candles[0].high
            dc_down = candles[0].low

            for candle in candles:
                if candle.high > dc_up:
                    dc_up = candle.high
                if candle.low < dc_down:
                    dc_down = candle.low

            dc_last_candle = candles[0].close
            return {
                    "up" : dc_up,
                    "down": dc_down,
                    "last_candle": dc_last_candle 
                    }
  
    def RSI_calc(self, coin, period):
        n = 0
        k = 0
        candles = helperdb.get_last_candles(coin, period, 15)
        if len(candles) < 15:
            return None
        else:
            cu = 0
            cd = 0
            for i in range(0, 14, 1):
                if candles[i].close - candles[i + 1].close >= 0:
                    cu += candles[i].close - candles[i + 1].close
                    n+=1
                else:
                    cd += candles[i].close - candles[i + 1].close
                    k+=1
            if n == 0:
                cu = 0
            else :
                cu /= n
            if k == 0:
                cd = 0
            else:
                cd /= k
            if cd == 0:
                return 100
            else :
                rs = cu/abs(cd)
                return 100*(1 - 1/(1 + rs))

    def BBP_calc(self, coin, period):
        candles = helperdb.get_last_candles(coin, period, 13)
        if len(candles) < 13:
            return None
        else:
            lwma_numerator_parts = []
            i = 0
            for candle in candles :
                lwma_numerator_parts.append(abs(i - 13 - 1)*candle.close)
                i+=1
            weight_sum = 0
            for i in range(1, 14, 1):
                weight_sum += abs(i - 13 - 1)
            lwma_13 = sum(lwma_numerator_parts)/weight_sum
            bulls = candles[0].high - lwma_13 
            bears = candles[0].low - lwma_13
            if bears == 0 :
                return 0
            else:
                return bulls/bears
    
    def MACD_calc(self, coin, period):
        pl = 34
        ps = 5
        pa = 5
        candles = helperdb.get_last_candles(coin, period, (pl*2)+1)
        if len(candles) < (pl*2+1):
            return {
                    "signal": None,
                    "macd": None
                    }
        else:
            emm_ps_arr = []
            emm_pl_arr = []
            macds = []
            emm_ps_arr = self.fill_ema_array(ps, candles, emm_ps_arr)
            emm_pl_arr = self.fill_ema_array(pl, candles, emm_pl_arr)
            for i in range(0,pa,1):
                macds.append(emm_ps_arr[i] - emm_pl_arr[i])
            signal = sum(macds)/pa
            macd = macds[0]

            return {
                    "signal": signal,
                    "macd": macd
                    }

    def AO_calc(self, coin, period):
        aol = 35;
        aos = 6;
        candles = helperdb.get_last_candles(coin, period, aol)

        if len(candles) < aol:
            return {
                    "f": None,
                    "s": None
                    } 
        else:
            sma_aol = 0
            for i in range(0, aol - 1, 1):
                sma_aol += (candles[i].high + candles[i].low)/2
            sma_aol /= aol - 1
            sma_aos = 0
            for i in range(0, aos -1, 1):
                sma_aos += (candles[i].high + candles[i].low)/2
            sma_aos /= aos - 1

            ao_1 = sma_aos - sma_aol

            sma_aol = 0
            for i in range(0, aol, 1):
                sma_aol += (candles[i].high + candles[i].low)/2
            sma_aol /= aol - 1
            sma_aos = 0
            for i in range(0, aos, 1):
                sma_aos += (candles[i].high + candles[i].low)/2
            sma_aos /= aos - 1

            ao_2 = sma_aos - sma_aol
            return {
                    "f": ao_1,
                    "s": ao_2
                    }

    def ADX_calc(self, coin , period): 
        candles = helperdb.get_last_candles(coin, period, 28)
        if len(candles) < 28:
            return None
        else:
            return self.adx(candles)

    def SO_calc(self, coin, period):
        candles = helperdb.get_last_candles(coin, period, 7)
        if len(candles) < 7:
            return None
        else:
            max_high = candles[0].high
            mix_low = candles[0].low
            for candle in candles:
                if candle.high > max_high:
                    max_high = candle.high
                if candle.low < min_low:
                    min_low = candle.low
            return 0 if max_high - min_low == 0 else 100*((candles[0].close - min_low)/(max_high-min_low))





math_helper = mathHelper()

