# helper for mat. models
import math

class matHelper(object):

    def fill_ema_array(self, period, candles, emm_arr):

        p = 2 / (period + 1)
        for i in range(period,-1,-1):
            if i == period:
                s = 0 
                for j in range(period + 1, (period * 2) + 1,1):
                    s += candles[j].close
                emm_arr[i] = s / period 
            else:
                emm_arr[i] = (candles[i].close * p ) + $emm_arr[i + 1] * (1 - p) 


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

math_helper = mathHelper()

