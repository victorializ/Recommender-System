import pandas as pd 
import numpy as np
from ast import literal_eval

from keys import Keys

def remove_spaces(string):
    return string.replace(" ", "")

def head(arr, N = 3):
    if len(arr) > N:
        arr = arr[:N]
    return arr

def get_values(arr):
    key = 'name'
    values = [str.lower(remove_spaces(obj[key])) for obj in arr]
    return values

def create_soup(features):
    def create(row):
        string = ' '
        for feature in features:
            string += ' '.join(head(row[feature]))
        return string   
    return create 


def add_soup(df, features, get_values=get_values):
    df1 = pd.DataFrame()

    for feature in features:
        df1[feature] = df[feature].copy().apply(literal_eval).apply(get_values)

    s = create_soup(features)
    df1[Keys.soup] = df1.apply(s, axis=1)
    df[Keys.soup] = df1[Keys.soup]
    return df