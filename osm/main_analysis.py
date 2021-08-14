# REFERENCE: https://stackoverflow.com/questions/33240427/getting-colorbar-instance-of-scatter-plot-in-pandas-matplotlib
# REFERENCE: https://jakevdp.github.io/PythonDataScienceHandbook/04.09-text-and-annotation.html
# REFERENCE: https://stackoverflow.com/questions/6774086/how-to-adjust-padding-with-cutoff-or-overlapping-labels

import sys
import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import seaborn
import ANOVA_analysis

seaborn.set()

def get_average_ratings_bar_graph(van_data):
    grouped_data = van_data.groupby('area_name').agg({'rating': 'mean', 'rating_num': 'count', 'is_franchise': 'sum'}).reset_index()
    ax = grouped_data.plot.barh(x="area_name", y="rating")
    ax.set_xlim([3.5,4.5])
    plt.xlabel("Rating n/5")
    plt.ylabel("Local Area Name")
    plt.subplots_adjust(bottom=0.15, left=0.25)
    
    plt.title("Average Google Maps Ratings for Restaurant for Vancouver's Local Areas")
    print(f"stats.normaltest p-value on rating: {stats.normaltest(van_data['rating']).pvalue}")

def get_ratings_histogram(van_data):
    plt.hist(van_data['rating'])
    plt.xlabel("Rating")
    plt.ylabel("Number of Restaurant Ratings")
    plt.title("Histogram of Restaurant Ratings")

def get_grouped_ratings_histogram(van_data):
    franchises = van_data.groupby('is_franchise').agg({'rating':'mean', 'rating_num':'count'})
    print(franchises)
    franchise_rating = van_data[van_data['is_franchise'] == True]['rating']
    non_franchise_rating = van_data[van_data['is_franchise'] == False]['rating']
    mann_pvalue = stats.mannwhitneyu(
        van_data[van_data['is_franchise'] == True]['rating'], 
        van_data[van_data['is_franchise'] == False]['rating'],
        alternative='two-sided'
    ).pvalue
    print(f"Mann Whiteyu p-value for franchise/non-franchise ratings: {mann_pvalue}")
    plt.title("Histogram of Franchise and Non-Franchise Restaurants Ratings")
    plt.xlabel("Rating")
    plt.ylabel("Number of Restaurants Ratings")
    plt.hist([franchise_rating,non_franchise_rating], label=['Non-franchise','Franchise'])
    plt.legend(loc='upper left')

def get_linear_regression(van_data): 
    van_data['is_franchise'] = (van_data['has_wikidata'] == True) | (van_data['count'] >= 5)
    grouped_data = van_data.groupby('area_name').agg({'rating': 'mean', 'rating_num': 'count', 'is_franchise': 'sum'}).reset_index()
    
    grouped_data['relative_franchise'] = grouped_data['is_franchise']/(grouped_data['rating_num'])
    # remove ratings less than 25
    grouped_data = grouped_data[grouped_data['rating_num'] >= 25]
    
    fit = stats.linregress(grouped_data['relative_franchise'], grouped_data['rating'])

    style = dict(size=9, color='#242424')
    ax = grouped_data.plot.scatter(x='relative_franchise', y='rating', c='rating_num', colormap='plasma')
    plt.plot(grouped_data['relative_franchise'], grouped_data['relative_franchise'] * fit.slope + fit.intercept, 'r-', linewidth=3, alpha=0.6)

    fig = plt.gcf()
    fig.get_axes()[1].set_ylabel("Number of Rated Restaurants")

    for _, row in grouped_data.iterrows():
        # fix graphical overlap on label
        if row['area_name'] in ["Downtown", "Kensington-Cedar Cottage"]:
            ax.text(row['relative_franchise'], row['rating']-0.010, row['area_name'], ha='center', **style)
        else:
            ax.text(row['relative_franchise'], row['rating']+0.005, row['area_name'], ha='center', **style)
    
    plt.title("Franchise Porportion vs Average Resturaunt Rating for a Local Area (with # of Ratings ≥ 25)")
    plt.xlabel("Franchise Restaurants Porportion")
    plt.ylabel("Average Ratings for an Area")
    plt.xticks(rotation=25)
    plt.subplots_adjust(bottom=0.15)
    print(f"Linear regerssion p-value: {fit.pvalue}")
    print(f"Linear regerssion slope: {fit.slope}")



def main(in_directory):
    van_data = pd.read_csv(in_directory, index_col=None)
    # remove ratings with under 20 ratings numbers
    van_data = van_data[van_data['rating_num'] >= 20]
    van_data['is_franchise'] = (van_data['has_wikidata'] == True) | (van_data['count'] >= 5)

    print("1: get_average_ratings_bar_graph")
    print("2: get_ratings_histogram")
    print("3: get_grouped_ratings_histogram")
    print("4: get_ratings_anova")
    print("5: get_linear_regression")
    analysis_type = input("Enter anaylsis type:")

    if analysis_type == '1':
        get_average_ratings_bar_graph(van_data)
    elif analysis_type == '2':
        get_ratings_histogram(van_data)
    elif analysis_type == '3':
        get_grouped_ratings_histogram(van_data)
    elif analysis_type == '4':
        ANOVA_analysis.get_ratings_anova(van_data)
    elif analysis_type == '5':
        get_linear_regression(van_data)
    else:
        print("Incorrect Input. Must be a 1-5.")
        return

    plt.show()


if __name__=='__main__':
    in_directory_main = sys.argv[1]
    main(in_directory_main)
