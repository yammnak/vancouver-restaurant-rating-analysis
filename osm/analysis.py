# REFERENCE: https://stackoverflow.com/questions/33240427/getting-colorbar-instance-of-scatter-plot-in-pandas-matplotlib
# REFERENCE: https://jakevdp.github.io/PythonDataScienceHandbook/04.09-text-and-annotation.html
# REFERENCE: https://stackoverflow.com/questions/6774086/how-to-adjust-padding-with-cutoff-or-overlapping-labels

import sys
import pandas as pd
from pandas.core.frame import DataFrame
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import numpy as np
import seaborn

seaborn.set()

def get_average_ratings_bar_graph(van_data):
    van_data['is_franchise'] = (van_data['has_wikidata'] == True) | (van_data['count'] >= 5)
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
    plt.title("Histogram of Restaurant Ratings in Vancouver")

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
    plt.title("Histogram of Restaurants Ratings")
    plt.xlabel("Rating")
    plt.ylabel("Number of Restaurants Ratings")
    plt.hist([franchise_rating,non_franchise_rating], label=['Non-franchise','Franchise'])
    plt.legend(loc='upper left')

def get_linear_regression(van_data): 
    van_data['is_franchise'] = (van_data['has_wikidata'] == True) | (van_data['count'] >= 5)
    grouped_data = van_data.groupby('area_name').agg({'rating': 'mean', 'rating_num': 'count', 'is_franchise': 'sum'}).reset_index()
    
    grouped_data['relative_franchise'] = grouped_data['is_franchise']/(grouped_data['rating_num'])
    grouped_data = grouped_data[grouped_data['area_name']!='Oakridge']
    fit = stats.linregress(grouped_data['relative_franchise'], grouped_data['rating'])

    style = dict(size=9, color='black')
    ax = grouped_data.plot.scatter(x='relative_franchise', y='rating', c='rating_num', colormap='viridis')
    plt.plot(grouped_data['relative_franchise'], grouped_data['relative_franchise'] * fit.slope + fit.intercept, 'r-', linewidth=3, alpha=0.6)

    fig = plt.gcf()
    fig.get_axes()[1].set_ylabel("Number of Rated Restaurants")

    for _, row in grouped_data.iterrows():
        ax.text(row['relative_franchise'], row['rating']+0.005, row['area_name'], ha='center', **style)
    
    plt.title("Linear Regression of Relative Franchise Porportion\n vs Average Rating for Restaurants a Local Area")
    plt.xlabel("Relative Franchise Restaurants Porportion")
    plt.ylabel("Average Ratings for an Area")
    plt.xticks(rotation=25)
    print(grouped_data)
    print("Linear regerssion p-value: {fit.pvalue}")


def get_ratings_anova(van_data):
    OUTPUT_TEMPLATE = (
        '"Do different areas in Vancouvers have different average ratings?" p-value:  {area_rating_p:.3g}\n'
        '"Do different areas in Vancouvers have different average ratings when franchises are not included?" p-value:  {non_franchise_area_rating_p:.3g}\n'
        '"Do different areas in Vancouvers have different average ratings when franchises and non-franchises with multiple stores are not included?" p-value:  {non_franchise_single_area_rating_p:.3g}\n'
        '"Do different areas in Vancouvers have different average ratings when areas with less than 25 total ratings are filtered out?" p-value:  {filtered_area_rating_p:.3g}\n'
        '"Do different areas in Vancouvers have different average ratings when franchises are not included and areas with less than 25 total ratings are filtered out?" p-value:  {filtered_non_franchise_area_rating_p:.3g}\n'
        '"Do different areas in Vancouvers have different average ratings when franchises and non-franchises with multiple stores are not included and areas with less than 25 total ratings are filtered out?" p-value:  {filtered_non_franchise_single_area_rating_p:.3g}\n'
    )

    def GetDropNAVars(df):
        ar = df['Arbutus-Ridge'].dropna()
        cbd = df['Downtown'].dropna()
        fair = df['Fairview'].dropna()
        gw = df['Grandview-Woodland'].dropna()
        hs = df['Hastings-Sunrise'].dropna()
        marp = df['Marpole'].dropna()
        rp = df['Riley Park'].dropna()
        shau = df['Shaughnessy'].dropna()
        stra = df['Strathcona'].dropna()
        we = df['West End'].dropna()
        ds = df['Dunbar-Southlands'].dropna()
        kerr = df['Kerrisdale'].dropna()
        kil = df['Killarney'].dropna()
        kits = df['Kitsilano'].dropna()
        sc = df['South Cambie'].dropna()
        vf = df['Victoria-Fraserview'].dropna()
        kc = df['Kensington-Cedar Cottage'].dropna()
        mp = df['Mount Pleasant'].dropna()
        oak = df['Oakridge'].dropna()
        rc = df['Renfrew-Collingwood'].dropna()
        sun = df['Sunset'].dropna()
        wpg = df['West Point Grey'].dropna()

        return ar, cbd, fair, gw, hs, marp, \
            rp, shau, stra, we, ds, kerr, kil, kits, sc, vf, \
            kc, mp, oak, rc, sun, wpg

    def GetAnovaPValue(df):
        ar, cbd, fair, gw, hs, marp, \
            rp, shau, stra, we, ds, kerr, kil, kits, sc, vf, \
            kc, mp, oak, rc, sun, wpg = GetDropNAVars(df)

        anova = stats.f_oneway(ar, cbd, fair, gw, hs, marp, \
            rp, shau, stra, we, ds, kerr, kil, kits, sc, vf, \
            kc, mp, oak, rc, sun, wpg)
        
        return anova.pvalue

    def CountLessThan25(df):
        return df.count() < 25

    non_franchises_multi = van_data.loc[(van_data['has_wikidata'] == False) & (van_data['count'] > 1) & (van_data['count'] < 5)]
    non_franchises_single = van_data.loc[(van_data['has_wikidata'] == False) & (van_data['count'] == 1)]
    non_franchises = van_data.loc[(van_data['has_wikidata'] == False) | (van_data['count'] < 5)]

    van_data_pivot = van_data.pivot(values = 'rating', columns = 'area_name')
    non_franchises_pivot = non_franchises.pivot(values = 'rating', columns = 'area_name')
    non_franchises_single_pivot = non_franchises_single.pivot(values = 'rating', columns = 'area_name')

    # Comparing ratings between areas including all stores
    areas_anova = GetAnovaPValue(van_data_pivot)
    areas_posthoc = pairwise_tukeyhsd(pd.to_numeric(van_data['rating']), van_data['area_name'], alpha = 0.05)

    # Comparing ratings between areas but not including franchises
    non_franchise_areas_anova = GetAnovaPValue(non_franchises_pivot)
    non_franchise_areas_posthoc = pairwise_tukeyhsd(pd.to_numeric(non_franchises['rating']), non_franchises['area_name'], alpha = 0.05)

    # Comparing ratings between areas but not including franchises and non-franchises with multiple stores
    non_franchise_single_areas_anova = GetAnovaPValue(non_franchises_single_pivot)
    non_franchise_single_areas_posthoc = pairwise_tukeyhsd(pd.to_numeric(non_franchises_single['rating']), non_franchises_single['area_name'], alpha = 0.05)

    ar, cbd, fair, gw, hs, marp, \
        rp, shau, stra, we, ds, kerr, kil, kits, sc, vf, \
        kc, mp, oak, rc, sun, wpg = GetDropNAVars(van_data_pivot)

    areas_anova_filtered = stats.f_oneway(cbd, fair, gw, hs, kc, kil, kits, marp, mp, rc, rp, \
        stra, sun, vf, we, wpg).pvalue
    non_franchise_areas_anova_filtered = stats.f_oneway(cbd, fair, gw, hs, kc, kits, marp, mp, rc, rp, \
        stra, sun, vf, we, wpg).pvalue
    non_franchise_single_areas_anova_filtered = stats.f_oneway(cbd, fair, gw, hs, kc, kits, marp, mp, rc, rp, \
        stra, sun, we, wpg).pvalue

    print(OUTPUT_TEMPLATE.format(
        area_rating_p = areas_anova,
        non_franchise_area_rating_p = non_franchise_areas_anova,
        non_franchise_single_area_rating_p = non_franchise_single_areas_anova,
        filtered_area_rating_p = areas_anova_filtered,
        filtered_non_franchise_area_rating_p = non_franchise_areas_anova_filtered,
        filtered_non_franchise_single_area_rating_p = non_franchise_single_areas_anova_filtered
    ))
    areas_posthoc.plot_simultaneous()
    plt.title('Tukey Posthoc Area Restaurant Ratings Comparison')
    plt.xlabel('Restuants Rating')
    plt.ylabel('Area Name')

def main(in_directory):
    van_data = pd.read_csv(in_directory, index_col=None)
    # remove ratings with under 20 ratings numbers
    van_data = van_data[van_data['rating_num'] >= 20]
    
    # COMMENT OUT ONE ANALYSIS AT A TIME:

    #get_average_ratings_bar_graph(van_data)
    get_ratings_histogram(van_data)
    #get_grouped_ratings_histogram(van_data)
    #get_ratings_anova(van_data)
    #get_linear_regression(van_data)

    
    plt.show()


if __name__=='__main__':
    in_directory_main = sys.argv[1]
    main(in_directory_main)
