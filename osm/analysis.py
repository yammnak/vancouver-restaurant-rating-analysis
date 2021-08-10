import sys
import pandas as pd
import gmplot
import area_finder as af

amenity_list = ["cafe", "pub", "restaurant", "fast_food", "bar"]
# Rough lat/lon boundaries for vancouver in case we need it
vancouver_north_lat = 49.317274
vancouver_south_lat = 49.198040
vancouver_west_lon = -132.225105
vancouver_east_lon = -123.023747

def has_wikidata(dictionary):
    return 'brand:wikidata' in dictionary.keys()

def get_area(lat, lon):
    pass


def main(in_directory):
    # apikey for the google maps plot
    apikey = 'AIzaSyCc3J7d3RwECUaAtYPZ2KfSK121UJDlnVc'

    van_data = pd.read_json(in_directory, lines=True)
    van_data = van_data.drop(['timestamp'], axis='columns')
    
    # mark each location with vancouver-local-area
    finder = af.AreaFinder()
    van_data['area_name'] = van_data.apply(lambda x: finder.get_area_name(x['lat'], x['lon']), axis='columns')
    # drop all outside the city of vancouver
    van_data = van_data.loc[(van_data['area_name'] != None)]

    # limit data by anemity_list and mark has_wikidata (assuming this means franchise)
    van_data = van_data.loc[van_data['amenity'].isin(amenity_list)]
    van_data['has_wikidata'] = van_data['tags'].apply(has_wikidata)

    # find resturant counts with the same name
    van_data_counts = van_data.groupby(['name']).count()
    van_data_counts = van_data_counts[['lat']]
    van_data_counts = van_data_counts.reset_index()
    van_data_counts = van_data_counts.rename({'lat': 'count'}, axis='columns')
    van_data = van_data.merge(van_data_counts, left_on='name', right_on='name')


    franchises = van_data.loc[(van_data['has_wikidata'] == True) | (van_data['count'] >= 5)]
    non_franchises_multi = van_data.loc[(van_data['has_wikidata'] == False) & (van_data['count'] > 1) & (van_data['count'] < 5)]
    non_franchises_single = van_data.loc[(van_data['has_wikidata'] == False) & (van_data['count'] == 1)]

    # non_franchises_multi.to_csv("output.csv")
    # print(non_franchises_multi)


if __name__=='__main__':
    in_directory_main = sys.argv[1]
    main(in_directory_main)
