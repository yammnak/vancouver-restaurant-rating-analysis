import sys
import pandas as pd
from pandas.core.frame import DataFrame
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import numpy as np

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
    str = df['Strathcona'].dropna()
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
        rp, shau, str, we, ds, kerr, kil, kits, sc, vf, \
        kc, mp, oak, rc, sun, wpg

def GetAnovaPValue(df):
    ar, cbd, fair, gw, hs, marp, \
        rp, shau, str, we, ds, kerr, kil, kits, sc, vf, \
        kc, mp, oak, rc, sun, wpg = GetDropNAVars(df)

    anova = stats.f_oneway(ar, cbd, fair, gw, hs, marp, \
        rp, shau, str, we, ds, kerr, kil, kits, sc, vf, \
        kc, mp, oak, rc, sun, wpg)
    
    return anova.pvalue

def CountLessThan25(df):
    return df.count() < 25

def main(in_directory):
    van_data = pd.read_csv(in_directory, index_col=None)
    
    # remove ratings with under 20 ratings numbers
    van_data = van_data[van_data['rating_num'] >= 20]
    avg_rating_data = van_data.groupby('area_name').mean()

    franchises = van_data.loc[(van_data['has_wikidata'] == True) | (van_data['count'] >= 5)]
    non_franchises_multi = van_data.loc[(van_data['has_wikidata'] == False) & (van_data['count'] > 1) & (van_data['count'] < 5)]
    non_franchises_single = van_data.loc[(van_data['has_wikidata'] == False) & (van_data['count'] == 1)]
    non_franchises = van_data.loc[(van_data['has_wikidata'] == False) | (van_data['count'] < 5)]

    van_data_pivot = van_data.pivot(values = 'rating', columns = 'area_name')
    non_franchises_pivot = non_franchises.pivot(values = 'rating', columns = 'area_name')
    non_franchises_single_pivot = non_franchises_single.pivot(values = 'rating', columns = 'area_name')

    # van_data.to_csv("analysis.csv")

    # Comparing ratings between areas including all stores
    areas_anova = GetAnovaPValue(van_data_pivot)
    areas_posthoc = pairwise_tukeyhsd(pd.to_numeric(van_data['rating']), van_data['area_name'], alpha = 0.05)
    # print(areas_posthoc)

    # Comparing ratings between areas but not including franchises
    non_franchise_areas_anova = GetAnovaPValue(non_franchises_pivot)
    non_franchise_areas_posthoc = pairwise_tukeyhsd(pd.to_numeric(non_franchises['rating']), non_franchises['area_name'], alpha = 0.05)
    # print(non_franchise_areas_posthoc)

    # Comparing ratings between areas but not including franchises and non-franchises with multiple stores
    non_franchise_single_areas_anova = GetAnovaPValue(non_franchises_single_pivot)
    non_franchise_single_areas_posthoc = pairwise_tukeyhsd(pd.to_numeric(non_franchises_single['rating']), non_franchises_single['area_name'], alpha = 0.05)
    # print(non_franchise_single_areas_posthoc)

    # Check if values change when excluding areas with less than 25 ratings

    # print(van_data_pivot.count() >= 25)
    # print(non_franchises_pivot.count() >= 25)
    # print(non_franchises_single_pivot.count() >= 25)

    ar, cbd, fair, gw, hs, marp, \
        rp, shau, str, we, ds, kerr, kil, kits, sc, vf, \
        kc, mp, oak, rc, sun, wpg = GetDropNAVars(van_data_pivot)

    areas_anova_filtered = stats.f_oneway(cbd, fair, gw, hs, kc, kil, kits, marp, mp, rc, rp, \
        str, sun, vf, we, wpg).pvalue
    non_franchise_areas_anova_filtered = stats.f_oneway(cbd, fair, gw, hs, kc, kits, marp, mp, rc, rp, \
        str, sun, vf, we, wpg).pvalue
    non_franchise_single_areas_anova_filtered = stats.f_oneway(cbd, fair, gw, hs, kc, kits, marp, mp, rc, rp, \
        str, sun, we, wpg).pvalue

    print(OUTPUT_TEMPLATE.format(
        area_rating_p = areas_anova,
        non_franchise_area_rating_p = non_franchise_areas_anova,
        non_franchise_single_area_rating_p = non_franchise_single_areas_anova,
        filtered_area_rating_p = areas_anova_filtered,
        filtered_non_franchise_area_rating_p = non_franchise_areas_anova_filtered,
        filtered_non_franchise_single_area_rating_p = non_franchise_single_areas_anova_filtered
    ))

if __name__=='__main__':
    in_directory_main = sys.argv[1]
    main(in_directory_main)
