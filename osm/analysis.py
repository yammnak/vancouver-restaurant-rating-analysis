import sys
import pandas as pd

def main(in_directory):
    van_data = pd.read_csv(in_directory, index_col=None)
    
    # remove ratings with under 20 ratings numbers
    van_data = van_data[van_data['rating_num'] >= 20]
    avg_rating_data = van_data.groupby('area_name').mean()


    '''
    franchises = van_data.loc[(van_data['has_wikidata'] == True) | (van_data['count'] >= 5)]
    non_franchises_multi = van_data.loc[(van_data['has_wikidata'] == False) & (van_data['count'] > 1) & (van_data['count'] < 5)]
    non_franchises_single = van_data.loc[(van_data['has_wikidata'] == False) & (van_data['count'] == 1)]
    '''

    print(van_data)
    print(avg_rating_data)
    van_data.to_csv("analysis.csv")

if __name__=='__main__':
    in_directory_main = sys.argv[1]
    main(in_directory_main)
