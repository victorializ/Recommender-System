from ast import literal_eval

from data.keys import Keys

def head(arr, N = 3):
    if len(arr) > N:
        arr = arr[:N]
    return arr

def extract_value(obj):
    key = "name"
    return obj[key]

def clean_value(value):
    return str.lower(value.replace(" ", ""))

def to_string(arr):
    return ' '.join(arr)

def find_director(arr):
    directors = []
    for obj in arr:
        if obj["job"] == 'Director':
            directors.append({"name": obj["name"]})
    return str(directors)

def to_string_of_values(arr):
    values = [clean_value(extract_value(obj)) for obj in head(literal_eval(arr))]
    return to_string(values)