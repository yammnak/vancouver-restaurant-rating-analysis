# REFRENCE: https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
# REFERENCE https://stackoverflow.com/questions/3193060/how-do-i-catch-a-specific-http-error-in-python
import sys
import pandas as pd
import urllib.request, json
import urllib.parse as up
from urllib.error import HTTPError

def get_ratings_data(fields):
    apikey = 'AIzaSyCEDEpNluqpYy_EzIAdlGT4DRiTP3_B99U'
    apifields = "fields=price_level,rating,user_ratings_total"
    apistr = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?key={apikey}&inputtype=textquery&{apifields}&"

    # call the google places api
    # print(apistr + fields)
    url = ""
    try:
        url = urllib.request.urlopen(apistr + fields)
    except HTTPError as err:
        if err.code == 500:
            return [None, None]
        else:
            raise
    if url == "":
        return
    data = json.loads(url.read().decode('utf-8'))
    if data['status'] != 'OK' or len(data['candidates']) == 0 or data['candidates'] == [{}]:
        return [None, None]
    return data['candidates'][0]['rating'], data['candidates'][0]['user_ratings_total']

def to_searchable(name: str):
    return up.quote(name)

def get_ratings(rating_data):
    return rating_data[0]

def get_ratings_num(rating_data):
    return rating_data[1]

def main(in_directory, out_directory):
    loc_data = pd.read_csv(in_directory, index_col=None)

    # get parameters for API call
    loc_data['parameters'] = "input="+loc_data['name'].apply(to_searchable)+"&point="+loc_data['lon'].astype(str)+","+loc_data['lat'].astype(str)
    # get rating information
    loc_data['rating_data'] = loc_data['parameters'].apply(get_ratings_data)
    loc_data['rating'] = loc_data['rating_data'].apply(get_ratings)
    loc_data['rating_num'] = loc_data['rating_data'].apply(get_ratings_num)
    
    loc_data = loc_data.drop(columns=['parameters', 'rating_data'])

    loc_data.to_csv(out_directory, index=False)
    
if __name__=='__main__':
    in_directory_main = sys.argv[1]
    out_directory_main = sys.argv[2]
    main(in_directory_main, out_directory_main)

# https://maps.googleapis.com/maps/api/place/findplacefromtext/json?key=AIzaSyCEDEpNluqpYy_EzIAdlGT4DRiTP3_B99U&inputtype=textquery&fields=price_level,rating,user_ratings_total&&input=Starbucks&point=-122.8589634,49.2769081
