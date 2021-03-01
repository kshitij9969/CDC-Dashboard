import pandas as pd

# RACE
race = dict()
race.update({1:"white"})
race.update({2:"black"})
race.update({3:"indian/native"})
race.update({4:"asian"})

# create dropdown options for RACE
race_options = []
for key, value in race.items():
    race_options.append({"label":value.title(), "value":value.title()})


# ETHNICITY
ethnicity = dict()
ethnicity.update({1:"non-hispanic"})
ethnicity.update({2:"hispanic"})
ethnicity.update({3:"unknown"})

# create dropdown options for ETHNICITY
ethnicity_options = []
for key, value in ethnicity.items():
    ethnicity_options.append({"label":value.title(), "value":value.title()})


# SEX
sex = dict()
sex.update({1:"male"})
sex.update({2:"female"})

# create dropdown options for SEX
sex_options = []
for key, value in sex.items():
    sex_options.append({"label":value.title(), "value":value.title()})


# AGE
age = dict()


# INTENT
intent = dict()
intent.update({0:"adverse effects"})
intent.update({1:"unintentional"})
intent.update({2:"suicide"})
intent.update({3:"homicide"})
intent.update({5:"undetermined intent"})
intent.update({6:"legal intervention"})
intent.update({7:"other specified"})

# create dropdown options for INTENT
intent_options = []
for key, value in intent.items():
    intent_options.append({"label":value.title(), "value":value.title()})


# CAUSES
df_causes = pd.read_csv("./data/Codebook_Cause_Labels.csv")
df_causes["cause"] = df_causes["cause"].astype("int")
df_causes["Causelbl"] = df_causes["Causelbl"].astype("str")
df_causes = df_causes.set_index("cause")
causes = dict()
for index, row in df_causes.iterrows():
    causes.update({index:row["Causelbl"].lower()})

# create dropdown options for CAUSES
causes_options = []
for key, value in causes.items():
    causes_options.append({"label":value.title(), "value":value.title()})

# COUNTY
df_county = pd.read_csv("./data/StateCounty_Labels.csv",dtype={"State": str,
                                                          "County":str})
df_county["county_fips"] = df_county["State"] + df_county["County"]
df_county = df_county.set_index("county_fips")
county = dict()
for index, row in df_county.iterrows():
    county.update({index:row["County_Name"]})

# create dropdown options for COUNTY
county_options = []
for key,value in county.items():
    county_options.append({"label":value, "value":key})


# STATE
df_state = df_county[["State","State_name"]].drop_duplicates()
df_state = df_state.set_index("State")
state = dict()
for index, row in df_state.iterrows():
    state.update({index:row["State_name"]})

print(state)

region = dict()
df_region = df_county[['Region', 'Region_name']].drop_duplicates()
df_region = df_region.set_index("Region")
for index, row in df_region.iterrows():
    region.update({index: row['Region_name']})

print(region)

# create dropdown options for STATE
state_options = []
for key,value in state.items():
    state_options.append({"label":value, "value":key})

# create dropdown options for MAP SCALE
map_scale_options = [{'value': 'state', 'label': 'States'},
                     {'value': 'county_fips', 'label': 'Counties'},
                     {'value': 'regional', 'label': 'Regional'}]

# create dropdown options for YEAR COMPARISON
analytics_options = [{'value': 'last_year', 'label' : 'Compare with year before selected'},
                     {'value': 'year_range', 'label': 'Compare range of years'},
                     {'value': 'combined_report', 'label' : 'Combined report: show intent with max death percentual      compared with year before'}]

# age ranges
age_ranges = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']
age_ranges_options = [{'value': i, 'label': f'{a}'} for i, a in enumerate(age_ranges)]

# State to Region Mapping
region_to_state = {
    "Region 1": ['Connecticut',
                    'Maine',
                    'Massachusetts',
                    'New Hampshire',
                    'Rhode Island',
                    'Vermont'
                 ],
    "Region 2": [
            "New Jersey",
            "New York",
            "Puerto Rico",
            "U.S. Virgin Islands"
    ],
    "Region 3": [
"Delaware",
"District of Columbia",
"Maryland",
"Pennsylvania",
"Virginia",
"West Virginia"
    ],
    "Region 4": [
"Alabama",
"Florida",
"Georgia",
"Kentucky",
"Mississippi",
"North Carolina",
"South Carolina",
"Tennessee"
    ],
    "Region 5": [
"Illinois",
"Indiana",
"Michigan",
"Minnesota",
"Ohio",
"Wisconsin"
    ],
    "Region 6": [
"Arkansas",
"Louisiana",
"New Mexico",
"Oklahoma",
"Texas"
    ],
    "Region 7": [
"Iowa",
"Kansas",
"Missouri",
"Nebraska"
    ],
    "Region 8": [
"Colorado",
"Montana",
"North Dakota",
"South Dakota",
"Utah",
"Wyoming"
    ],
    "Region 9": [
"American Samoa ",
"Arizona",
"California",
"Commonwealth of the Northern Mariana Islands",
"Federated States of Micronesia",
"Guam",
"Hawaii",
"Nevada",
"Republic of Palau",
"Republic of the Marshall Islands"
    ],
    "Region 10": [
"Alaska",
"Idaho",
"Oregon",
"Washington"
    ]
}

