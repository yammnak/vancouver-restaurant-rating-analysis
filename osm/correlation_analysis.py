import sys
import pandas as pd
from pandas.core.frame import DataFrame
from scipy import stats
from scipy.stats.mstats_basic import linregress
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import numpy as np
import seaborn
import math

seaborn.set()

def main(in_directory):
    van_data = pd.read_csv(in_directory, index_col=None)
    # remove ratings with under 20 ratings numbers
    van_data = van_data[van_data['rating_num'] >= 20]
    print(van_data)


    van_data['is_franchise'] = (van_data['has_wikidata'] == True) | (van_data['count'] >= 5)
    van_data['not_franchise'] = van_data['is_franchise'] == False
    grouped_data = van_data.groupby('area_name').agg({'rating': 'mean', 'is_franchise': 'sum', 'not_franchise': 'sum'}).reset_index()

    grouped_data['relative_franchise'] = grouped_data['is_franchise']/(grouped_data['not_franchise'] + grouped_data['is_franchise'])
    grouped_data['total_stores'] = grouped_data['is_franchise'] + grouped_data['not_franchise']
    filtered_data = grouped_data
    # Filter out areas with less than 25 stores as low totals affect the relative_franchise percentage too much
    filtered_data = filtered_data[filtered_data['total_stores'] >= 25]
    
    print(stats.normaltest(van_data['rating']).pvalue)


    '''
    plt.hist(van_data['rating'])
    plt.xlabel("Rating")
    plt.title("Histogram of Resturaunt Ratings in Vancouver")
    '''

    '''
    ax = grouped_data.plot.barh(x="area_name", y="rating")
    ax.set_xlim([3.5,4.5])
    plt.xlabel("Rating n/5")
    plt.ylabel("Local Area Name")
    plt.title("Average Google Maps Ratings for Resturuants for Vancouver's Local Areas")
    '''

    R = np.corrcoef(filtered_data['relative_franchise'], filtered_data['rating'])
    linreg = stats.linregress(filtered_data['relative_franchise'], filtered_data['rating'])
    prediction = linreg.slope*filtered_data['relative_franchise'] + linreg.intercept
    plt.plot(filtered_data['relative_franchise'], filtered_data['rating'], 'b.', label = 'data')
    plt.plot(filtered_data['relative_franchise'], prediction, 'g-', label = 'fit')
    plt.xlabel('Relative Percentage of Franchises per Area')
    plt.ylabel('Average Rating')
    plt.title('Average Rating vs Relative Percentage of Franchises per Area')
    plt.legend()
    plt.show()

    print(R)
    print(linreg.pvalue)


if __name__=='__main__':
    in_directory_main = sys.argv[1]
    main(in_directory_main)
