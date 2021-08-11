import sys
import pandas as pd

def main(in_directory, out_directory):
    van_data = pd.read_csv(in_directory, index_col=None)
    
    franchises = van_data.loc[(van_data['has_wikidata'] == True) | (van_data['count'] >= 5)]
    non_franchises_multi = van_data.loc[(van_data['has_wikidata'] == False) & (van_data['count'] > 1) & (van_data['count'] < 5)]
    non_franchises_single = van_data.loc[(van_data['has_wikidata'] == False) & (van_data['count'] == 1)]

    print(van_data)
    van_data.to_csv(out_directory)

if __name__=='__main__':
    in_directory_main = sys.argv[1]
    out_directory_main = sys.argv[2]
    main(in_directory_main, out_directory_main)
