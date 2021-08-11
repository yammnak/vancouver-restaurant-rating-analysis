import sys
import pandas as pd
import area_finder as af

amenity_list = ["cafe", "pub", "restaurant", "fast_food", "bar"]

def has_wikidata(dictionary):
    return 'brand:wikidata' in dictionary.keys()

def main(in_directory, out_directory):
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
    # write to outfile
    van_data.to_csv(out_directory, index=False)

if __name__=='__main__':
    in_directory_main = sys.argv[1]
    out_directory_main = sys.argv[2]
    main(in_directory_main, out_directory_main)
