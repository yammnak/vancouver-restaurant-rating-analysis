# OSM CMPT 353 Project - Examining Vancouver's Local Areas and Restaurant Ratings
Using data analysis tools, we wanted to determine if certain local areas in the city had a higher proportion of well-rated restaurants. We also wanted to examine if there was a significant difference in average ratings between franchises and independently owned restaurants. Lastly, we wanted to investigate if there was a meaningful correlation between the proportion of franchise restaurants in an area and the average ratings in that area.

## Required Libraries
- pandas
- scipy
- statsmodels
- matplotlib
- seaborn
- jupyter
- shapely
- numpy

## File List
- Python Files (in `osm/`)
    + `ANOVA_analysis.py`: function for ANOVA analysis
    + `area_finder.py`: class for determining which local area a lat/lon point belongs to
    + `heatmaps.ipynb`: jupyiter notebook for producing heatmaps
    + `get_van_data.py`: performs data cleaning on larger amenities dataset to produce a csv
    + `google_ratings.py`: appends Google Places API rating to locations to produce a csv
    + `main_analysis.py`: performs different kinds of data analysis chosen by the user
- Data Files (in `osm/`)
    + `amenities-vancouver.json.gz`: Extracted Vancouver data from planet.osm (given in project files)
    + `local-area-boundary.json`: City of Vancouver's local area boundaries provided by their [Open Data Portal](https://opendata.vancouver.ca/explore/dataset/local-area-boundary/information/)
    + `van_data.csv`: csv produced by `get_van_data.py` using `amenities-vancouver.json.gz`
    + `van_data_rated.csv`: csv produced by `google_ratings.py` using `van_data.csv`


## How to Run Code
### Data Cleaning to Produce needed for van_data_rated.csv (NOT RECOMMENDED)
1. `python3 get_van_data.py amenities-vancouver.json.gz van_data.csv`
    + This produces a cleaned up .csv from the larger dataset.
2. `python3 google_ratings.py van_data.csv van_data_rated.csv`
    + Because of the API calls required, this step takes about 20 minutes and costs money.
    + If you want to test the functionality, do it with a smaller dataset.
        * `python3 google_ratings.py test_data.csv test_data_rated.csv`

### Data Analysis
- `python3 main_analysis.py van_data_rated.csv`
    + The program accepts an integer input via console
        1: Get Average Ratings Bar Graph
        2. Get Ratings Histogram
        3. Get Grouped Ratings Histogram
        4. Get Ratings ANOVA for Local Areas
        5. Get Linear Regression for Franchise Proportion Boundaries vs. Average Rating Local Areas.
- Run the `heatmaps.ipynb` Jupyiter notebook for heatmaps. 