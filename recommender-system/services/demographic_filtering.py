#Generalized recommendations to every user, based on item popularity

import pandas
import numpy

from data.keys import Keys

def general_rate(data, avarage_key=Keys.avarage, count_key=Keys.count, q=0.9):
    #data - pandas DataFrame
    #avarage_key - name of the column with avarage vote
    #count_key - name of the column with number of votes
    #q - cutoff percentile
    C = data[avarage_key].mean() #mean vote across the whole report
    m = data[count_key].quantile(q) #minimum votes required to be listed in the chart
    q_items = data.copy().loc[data[count_key] >= m] #items with required votes number
    def weighted_rating(item):
        v = item[count_key]
        R = item[avarage_key]
        # Calculation based on the IMDB formula
        return (v/(v+m) * R) + (m/(m+v) * C)
    q_items[Keys.score] = q_items.apply(weighted_rating, axis=1)
    q_items = q_items.sort_values(Keys.score, ascending=False)
    return q_items