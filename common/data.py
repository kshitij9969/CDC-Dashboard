# import os
#
# import pandas as pd
# import common.mapping as mapping
# from datetime import datetime
#
# print("loading dataset...")
#
# df_state_grouped = None
# df_county_grouped = None
# df_region_grouped = None
#
#
# def get_grouped_data(df_mortality):
#     """
#         Prepares and returns grouped datasets
#     """
#     global df_state_grouped, df_county_grouped, df_region_grouped
#
#     if df_state_grouped is None:
#         df_county_grouped = df_mortality.pivot_table(
#             index=['state', 'region', 'county', 'age_range', 'race', 'sex', 'ethnicity', 'cause', 'intent'],
#             columns=['year_i'],
#             values='deaths',
#             aggfunc='sum').fillna(0).reset_index()
#         df_county_grouped = pd.merge(df_county_grouped, mapping.df_county, left_on=['state', 'region', 'county'],
#                                      right_on=['State', 'Region', 'County'], how='inner')
#
#         df_county_grouped['County_Name_Full'] = df_county_grouped['County_Name'] + ',' + df_county_grouped['State_name']
#
#         cols_state = ['state', 'State_name', 'age_range', 'race', 'sex', 'ethnicity', 'cause', 'intent']
#         cols_region = ['region', 'Region_name', 'age_range', 'race', 'sex', 'ethnicity', 'cause', 'intent']
#         years = df_mortality['year_i'].unique()
#         df_state_grouped = df_county_grouped.groupby(cols_state)[years].sum().reset_index()
#         df_region_grouped = df_county_grouped.groupby(cols_region)[years].sum().reset_index()
#
#     return df_state_grouped, df_county_grouped, df_region_grouped
#
#
# def load_dataset(df_mortality_feather_path, df_mortality_csv_path,
#                  df_mortality_state_feather_path,
#                  df_mortality_county_feather_path,
#                  df_mortality_region_feather_path,):
#     global df_region_grouped, df_county_grouped, df_state_grouped
#     if not os.path.isfile(df_mortality_feather_path):
#
#         df_mortality = pd.read_csv(df_mortality_csv_path, dtype={"state": str, "county": str})
#
#         df_mortality["year"] = df_mortality["year"].apply(lambda x: datetime(x, 1, 1, 0, 0, 0))
#         df_mortality["sex"] = df_mortality["sex"].apply(lambda x: mapping.sex[x])
#         df_mortality["race"] = df_mortality["race"].apply(lambda x: mapping.race[x])
#         df_mortality["ethnicity"] = df_mortality["ethnicity"].apply(lambda x: mapping.ethnicity[x])
#         df_mortality["cause"] = df_mortality["cause"].apply(lambda x: mapping.causes[x])
#         df_mortality["intent"] = df_mortality["intent"].apply(lambda x: mapping.intent[x])
#
#         df_mortality["county_fips"] = df_mortality["state"] + df_mortality["county"]
#         df_mortality["state_name"] = df_mortality["state"].apply(lambda x: mapping.state[x])
#         df_mortality["county_name"] = df_mortality["county_fips"].apply(lambda x: mapping.county[x])
#
#         df_mortality["age"] = df_mortality["age"].apply(lambda x: int((x if x < 90 else 89) / 10))
#         df_mortality["age_range"] = df_mortality["age"].apply(lambda x: mapping.age_ranges[x])
#         df_mortality['year_i'] = df_mortality['year'].dt.year
#
#
#         # initialize datasets
#         get_grouped_data(df_mortality)
#
#         df_mortality.to_feather(df_mortality_feather_path)
#         df_state_grouped.columns = df_state_grouped.columns.astype(str)
#         df_state_grouped['age_range_all'] = 'All'
#         df_state_grouped['race_all'] = 'All'
#         df_state_grouped['sex_all'] = 'All'
#         df_state_grouped['ethnicity_all'] = 'All'
#         df_state_grouped.to_feather(df_mortality_state_feather_path)
#         df_state_grouped.columns = [c if not c.startswith('2') else int(c) for c in df_state_grouped.columns]
#         df_county_grouped.columns = df_county_grouped.columns.astype(str)
#         df_county_grouped['age_range_all'] = 'All'
#         df_county_grouped['race_all'] = 'All'
#         df_county_grouped['sex_all'] = 'All'
#         df_county_grouped['ethnicity_all'] = 'All'
#         df_county_grouped.to_feather(df_mortality_county_feather_path)
#         df_county_grouped.columns = [c if not c.startswith('2') else int(c) for c in df_county_grouped.columns]
#
#         df_region_grouped.columns = df_region_grouped.columns.astype(str)
#         df_region_grouped['age_range_all'] = 'All'
#         df_region_grouped['race_all'] = 'All'
#         df_region_grouped['sex_all'] = 'All'
#         df_region_grouped['ethnicity_all'] = 'All'
#         df_region_grouped.to_feather(df_mortality_region_feather_path)
#         df_region_grouped.columns = [c if not c.startswith('2') else int(c) for c in df_region_grouped.columns]
#
#     else:
#
#         df_mortality = pd.read_feather(df_mortality_feather_path)
#         df_state_grouped = pd.read_feather(df_mortality_state_feather_path)
#         df_state_grouped.columns = [c if not c.startswith('2') else int(c) for c in df_state_grouped.columns]
#         df_county_grouped = pd.read_feather(df_mortality_county_feather_path)
#         df_county_grouped.columns = [c if not c.startswith('2') else int(c) for c in df_county_grouped.columns]
#         df_region_grouped = pd.read_feather(df_mortality_region_feather_path)
#         df_region_grouped.columns = [c if not c.startswith('2') else int(c) for c in df_region_grouped.columns]
#
#     year_series = df_mortality["year"].drop_duplicates().sort_values()
#     year_options = []
#     for key, value in year_series.iteritems():
#         year_options.append({"label": value.year, "value": value.year})
#     year_options_max = max(year_series).year
#     year_options_min = min(year_series).year
#     return year_series, year_options, year_options_max, year_options_min, df_mortality
#
# print("DONE!")

import os

import pandas as pd
import common.mapping as mapping
from datetime import datetime

print("loading dataset...")

df_state_grouped = None
df_county_grouped = None
df_region_grouped = None


def get_grouped_data():
    """
        Prepares and returns grouped datasets
    """
    global df_state_grouped, df_county_grouped, df_region_grouped

    if df_state_grouped is None:
        df_county_grouped = df_mortality.pivot_table(
            index=['state', 'region', 'county', 'age_range', 'race', 'sex', 'ethnicity', 'cause', 'intent'],
            columns=['year_i'],
            values='deaths',
            aggfunc='sum').fillna(0).reset_index()
        df_county_grouped = pd.merge(df_county_grouped, mapping.df_county, left_on=['state', 'region', 'county'],
                                     right_on=['State', 'Region', 'County'], how='inner')

        df_county_grouped['County_Name_Full'] = df_county_grouped['County_Name'] + ',' + df_county_grouped['State_name']

        cols_state = ['state', 'State_name', 'age_range', 'race', 'sex', 'ethnicity', 'cause', 'intent']
        cols_region = ['region', 'Region_name', 'age_range', 'race', 'sex', 'ethnicity', 'cause', 'intent']
        years = df_mortality['year_i'].unique()
        df_state_grouped = df_county_grouped.groupby(cols_state)[years].sum().reset_index()
        df_region_grouped = df_county_grouped.groupby(cols_region)[years].sum().reset_index()

    return df_state_grouped, df_county_grouped, df_region_grouped


if not os.path.isfile("./data/MortalityData_2001_2018_Final_v2.feather"):

    df_mortality = pd.read_csv("./data/MortalityData_2001_2018_Final_v2.csv", dtype={"state": str, "county": str})

    df_mortality["year"] = df_mortality["year"].apply(lambda x: datetime(x, 1, 1, 0, 0, 0))
    df_mortality["sex"] = df_mortality["sex"].apply(lambda x: mapping.sex[x])
    df_mortality["race"] = df_mortality["race"].apply(lambda x: mapping.race[x])
    df_mortality["ethnicity"] = df_mortality["ethnicity"].apply(lambda x: mapping.ethnicity[x])
    df_mortality["cause"] = df_mortality["cause"].apply(lambda x: mapping.causes[x])
    df_mortality["intent"] = df_mortality["intent"].apply(lambda x: mapping.intent[x])

    df_mortality["county_fips"] = df_mortality["state"] + df_mortality["county"]
    df_mortality["state_name"] = df_mortality["state"].apply(lambda x: mapping.state[x])
    df_mortality["county_name"] = df_mortality["county_fips"].apply(lambda x: mapping.county[x])

    df_mortality["age"] = df_mortality["age"].apply(lambda x: int((x if x < 90 else 89) / 10))
    df_mortality["age_range"] = df_mortality["age"].apply(lambda x: mapping.age_ranges[x])
    df_mortality['year_i'] = df_mortality['year'].dt.year


    # initialize datasets
    get_grouped_data()

    df_mortality.to_feather("./data/MortalityData_2001_2018_Final_v2.feather")
    df_state_grouped.columns = df_state_grouped.columns.astype(str)
    df_state_grouped['age_range_all'] = 'All'
    df_state_grouped['race_all'] = 'All'
    df_state_grouped['sex_all'] = 'All'
    df_state_grouped['ethnicity_all'] = 'All'
    df_state_grouped.to_feather("./data/MortalityData_2001_2018_SG_v2.feather")
    df_state_grouped.columns = [c if not c.startswith('2') else int(c) for c in df_state_grouped.columns]
    df_county_grouped.columns = df_county_grouped.columns.astype(str)
    df_county_grouped['age_range_all'] = 'All'
    df_county_grouped['race_all'] = 'All'
    df_county_grouped['sex_all'] = 'All'
    df_county_grouped['ethnicity_all'] = 'All'
    df_county_grouped.to_feather("./data/MortalityData_2001_2018_CG_v2.feather")
    df_county_grouped.columns = [c if not c.startswith('2') else int(c) for c in df_county_grouped.columns]

    df_region_grouped.columns = df_region_grouped.columns.astype(str)
    df_region_grouped['age_range_all'] = 'All'
    df_region_grouped['race_all'] = 'All'
    df_region_grouped['sex_all'] = 'All'
    df_region_grouped['ethnicity_all'] = 'All'
    df_region_grouped.to_feather("./data/MortalityData_2001_2018_RG_v2.feather")
    df_region_grouped.columns = [c if not c.startswith('2') else int(c) for c in df_region_grouped.columns]

else:

    df_mortality = pd.read_feather("./data/MortalityData_2001_2018_Final_v2.feather")
    df_state_grouped = pd.read_feather("./data/MortalityData_2001_2018_SG_v2.feather")
    df_state_grouped.columns = [c if not c.startswith('2') else int(c) for c in df_state_grouped.columns]
    df_county_grouped = pd.read_feather("./data/MortalityData_2001_2018_CG_v2.feather")
    df_county_grouped.columns = [c if not c.startswith('2') else int(c) for c in df_county_grouped.columns]
    df_region_grouped = pd.read_feather("./data/MortalityData_2001_2018_RG_v2.feather")
    df_region_grouped.columns = [c if not c.startswith('2') else int(c) for c in df_region_grouped.columns]

year_series = df_mortality["year"].drop_duplicates().sort_values()
year_options = []
for key, value in year_series.iteritems():
    year_options.append({"label": value.year, "value": value.year})
year_options_max = max(year_series).year
year_options_min = min(year_series).year

print("DONE!")

