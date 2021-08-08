import sys
import pandas as pd
import gmplot

amenitiy_list = ["cafe", "pub", "restaurant", "fast_food", "bar"]

def has_wikidata(dictionary):
    return 'brand:wikidata' in dictionary.keys()

def main(in_directory):
    # apikey for the google maps plot
    apikey = 'AIzaSyCc3J7d3RwECUaAtYPZ2KfSK121UJDlnVc'

    van_data = pd.read_json(in_directory, lines=True)
    van_data = van_data.drop(['timestamp'], axis='columns')
    van_data = van_data.loc[van_data['amenity'].isin(amenitiy_list)]
    van_data['has_wikidata'] = van_data['tags'].apply(has_wikidata)

    van_data_counts = van_data.groupby(['name']).count()
    van_data_counts = van_data_counts[['lat']]
    van_data_counts = van_data_counts.reset_index()
    van_data_counts = van_data_counts.rename({'lat': 'count'}, axis='columns')
    print(van_data_counts)

    van_data = van_data.merge(van_data_counts, left_on='name', right_on='name')

    # van_data.to_csv("output.csv")
    print(van_data)

    gmap = gmplot.GoogleMapPlotter(49.246292, -123.116226, 12, apikey=apikey)
    gmap.heatmap(van_data['lat'], van_data['lon'])
    gmap.draw('test.html')

if __name__=='__main__':
    in_directory_main = sys.argv[1]
    main(in_directory_main)
