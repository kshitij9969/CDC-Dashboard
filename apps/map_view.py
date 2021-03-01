import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import common.filtering as filtering
import common.mapping as mapping
import json
from app import cache
from app import app
from urllib.request import urlopen
from common.header import header_layout
from common.data import df_mortality
from common.data import year_options
from common.data import year_options_max
from common.data import year_options_min
from common.mapping import race_options
from common.mapping import sex_options
from common.mapping import ethnicity_options
from common.mapping import intent_options
from common.mapping import causes_options
from common.mapping import state_options
from common.mapping import map_scale_options
from common.mapping import analytics_options
from common.mapping import age_ranges_options

filter_layout = html.Div([
    html.Div([
        html.Div([
           html.Div([
               html.Label("Sex"),
               dcc.Dropdown(
                   id="Sex",
                   options=sex_options,
                   placeholder="Select",
                   multi=True
               ),
           ]),
           html.Div([
               html.Label("Race"),
               dcc.Dropdown(
                   id="Race",
                   options=race_options,
                   placeholder="Select",
                   multi=True
               )
           ]),
           html.Div([
               html.Label("Ethnicity"),
               dcc.Dropdown(
                   id="Ethnicity",
                   options=ethnicity_options,
                   placeholder="Select",
                   multi=True
               ),
           ]),
           html.Div([
               html.Label("Intent"),
               dcc.Dropdown(
                   id="Intent",
                   options=intent_options,
                   placeholder="Select",
                   multi=True
               ),
           ]),
           html.Div([
              html.Label("Causes"),
              dcc.Dropdown(
                  id="Cause",
                  options=causes_options,
                  placeholder="Select",
                  multi=True
              ),
            ]),
        ], className="row"),

        html.Div([
            html.Div([
                html.Label("Age"),
                dcc.Dropdown(
                    id="Age",
                    options=age_ranges_options,
                    placeholder="Select",
                    multi=True
                ),
            ]),
        ], className="row"),
    ], id="filter_layout"),
    html.Div([
        html.Div([
          html.Label("State"),
          dcc.Dropdown(
              id="State",
              options=state_options,
              placeholder="Select",
              multi=True
          ),
        ], id="state_choice"),
    ], className="row")
])

year_choice_layout = html.Div([
    html.Div([
          html.Label("Year"),
          dcc.Dropdown(
              id="year",
              options=year_options[1:],
              value=year_options_max,
              clearable=False,
              multi=False
          )
    ])
], id="year_choice", className="row")

year_range_layout = html.Div([
    html.Div([
        html.Div([
            html.Label("Comparison Years"),
                 dcc.RangeSlider(
                     id="years_comparison",
                     min=year_options_min,
                     max=year_options_max,
                     step=1,
                     value=[year_options_max-1, year_options_max-1],
                     marks={
                         year_options_min:str(year_options_min),
                         2000:"2000",
                         2005:"2005",
                         2010:"2010",
                         2015:"2015",
                         year_options_max:str(year_options_max),
                    }
                 )
            ]),

        html.Div([
           html.Label("Base Years"),
               dcc.RangeSlider(
                   id="years_base",
                   min=year_options_min,
                   max=year_options_max,
                   step=1,
                   value=[year_options_max, year_options_max],
                   marks={
                       year_options_min:str(year_options_min),
                       2000:"2000",
                       2005:"2005",
                       2010:"2010",
                       2015:"2015",
                       year_options_max:str(year_options_max),
                   }
               )
           ]),
    ], className="row"),
], id="year_range", style={"display": "none"})


layout = html.Div([
    header_layout,
    html.Div([
        html.Div([
        html.Div([
               html.Label("Detail level"),
               dcc.Dropdown(
                      id="map_scale",
                      options=map_scale_options,
                      value="state",
                      clearable=False,
                      multi=False
               )
           ]),
            html.Div([
                html.Label("Analytics options"),
                dcc.Dropdown(
                    id="analytics_option",
                    options=analytics_options,
                    value="last_year",
                    clearable=False,
                    multi=False,
                    optionHeight=60
                )
            ],
            #     style={
            #     'white-space': 'nowrap',
            #     'overflow': 'scroll',
            #     'text-overflow': 'ellipsis'
            # }
            ),
            year_choice_layout,
            year_range_layout,
            filter_layout,
        ], className="three columns"),
        html.Div([
        html.Div([html.Label("Summary"),html.Div(id="output_years_range_text")], style={
            'textAlign': 'center',
            'fontWeight': 'bold',
        }),
            dcc.Graph(id="Map", className="nine columns",
                      style={
                          "height": '100%'
                      }),
        ])
    ], style={
        'height': '100%'
    },
        className="row"),
    # html.Div(id="link_div"),
    # html.Div([
    #
    #    ], className="row"),

])

json_file = './data/geojson-counties-fips.json'
if not os.path.isfile(json_file):
    with open(json_file, 'w') as f:
        f.write(urlopen("https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json")
                .read().decode())

with open(json_file, 'r') as f:
    counties = json.load(f)

json_file = './data/gz_2010_us_040_00_5m.json'
if not os.path.isfile(json_file):
    # https://eric.clst.org/tech/usgeojson/
    with open(json_file, 'w') as f:
        f.write(urlopen("https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_040_00_5m.json")
                .read().decode())

with open(json_file, 'r') as f:
    states = json.load(f)

@app.callback(
    dash.dependencies.Output("state_choice", "style"),
    dash.dependencies.Input("map_scale", "value")
)
def update_state_choice(map_scale):
    if map_scale == "county_fips":
        return {"display":"inline"}
    else:
        return {"display":"none"}

@app.callback(
     dash.dependencies.Output("output_years_range_text", "children"),
    [dash.dependencies.Input("years_base", "value"),
     dash.dependencies.Input("years_comparison", "value")]
)
def update_output_years_text(years_base,years_comparison):
    output_years_range_text = "Comparing [{},{}] with [{},{}]".format(years_comparison[0],years_comparison[1],years_base[0],years_base[1])
    return output_years_range_text

@app.callback(
    [dash.dependencies.Output("year_choice", "style"),
     dash.dependencies.Output("year_range", "style"),
     dash.dependencies.Output("filter_layout", "style")],
     dash.dependencies.Input("analytics_option", "value"),
)
def hide_filter_options(analytics_option):
    if analytics_option == "year_range":
        year_range  = {"display":"inline"}
        year_choice = {"display":"none"}
        filter_layout = {"display":"inline"}
    elif analytics_option == "combined_report":
        year_range  = {"display":"none"}
        year_choice = {"display":"inline"}
        filter_layout = {"display":"none"}
    else:
        year_range  = {"display":"none"}
        year_choice = {"display":"inline"}
        filter_layout = {"display":"inline"}

    return year_choice, year_range, filter_layout

@app.callback(
    dash.dependencies.Output("link_div", "children"),
    dash.dependencies.Input('Map', 'clickData')
)
def map_click_handler(clickData):
    if clickData == None:
        link = ''
    else:
        #placeholder, probably dcc.Location is the desired routing option,
        #when the destination is defined
        url = "Click to go to the territory link: https://localhost:8050/" + clickData['points'][0]['hovertext']
        link = dcc.Link(url, href=url)
    return link


# Helper function for color scale display
def normalize(value, min_value, max_value):
    norm = (value-min_value)/abs(max_value-min_value)
    if   norm > 1 : norm = 1
    elif norm < 0 : norm = 0
    return norm


def generate_map_fig(df,map_scale,hover_data):
    if map_scale == "county_fips":
        geojson = counties
        # print(counties)
        featureidkey="id"
        locations = "county_fips"
        df["hover_name"] = df[locations].apply(lambda x: mapping.county[x])
    elif map_scale == 'state':
        geojson = states
        # print(states)
        featureidkey="properties.STATE"
        locations = "state"
        df["hover_name"] = df[locations].apply(lambda x: mapping.state[x])
        print(df)
    else:
        geojson = states
        featureidkey = 'properties.STATE'
        locations = 'state'
        regions = list(range(1, 10))
        df_temp = pd.read_csv("/Users/kshitijsingh/Downloads/tc-cdc-dashboard-main/data/StateCounty_Labels.csv", usecols=['State', 'Region'])
        df_temp.drop_duplicates(inplace=True)
        dict1 = dict()
        for index, row in df_temp.iterrows():
            dict1[int(row['State'])] = row['Region']
        df['region'] = df['state'].apply(lambda state: dict1[int(state)])
        for region in regions:
            sum_x = df[df['region'] == region]['deaths_x'].sum()
            sum_y = df[df['region'] == region]['deaths_y'].sum()
            change = (sum_y - sum_x)/sum_x
            df.loc[df['region'] == region, 'deaths_change'] = change
        df["hover_name"] = df['region'].apply(lambda x: mapping.region[x]) + ',' + df['state'].apply(lambda x: mapping.state[x])
        df = df[['state', 'deaths_x', 'deaths_y', 'deaths_change', 'hover_name']]
        print(df)
        # df['hover_name'] = df[locations].apply(lambda x: mapping.region[x])

    # criteria and threshold for map colors
    if not df.empty:
        df_min = df["deaths_change"].min()
        df_max = df["deaths_change"].max()
        color_continuous_scale=[(0,                             "green"),
                                (normalize(-0.1,df_min,df_max), "beige"),
                                (normalize( 0.1,df_min,df_max), "beige"),
                                (1,                             "red"  )]
    else:
        color_continuous_scale=[(0,                             "green")]

    fig = px.choropleth_mapbox(df, geojson=geojson, locations=locations, color="deaths_change",
                               featureidkey=featureidkey,
                               color_continuous_scale=color_continuous_scale,
                               mapbox_style="carto-positron",
                               hover_name="hover_name",
                               hover_data=hover_data,
                               zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                               opacity = 0.9,
                               labels={"deaths_change":"deaths_change"},
                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(coloraxis_colorbar=dict(tickformat=".2%"))
    # chorpleth = go.Choropleth(
    #     locationmode='USA-states',
    #     z=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     locations=['ND', 'SD', 'NE', 'KS', 'MO', 'IA', 'MN', 'WI', 'MI', 'IL', 'IN', 'OH'],
    #     colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
    #     marker_line_color='Blue',
    #     showscale=False,
    # )
    # fig = px.choropleth(locations=["CA", "TX", "NY"], locationmode="USA-states", color=['Blue', "Blue", "Blue"], hover_data=[], scope="usa")
    return fig


@cache.memoize()
def combined_report_data(map_scale, filter_list, state):
    """ Creates and caches data for a combined report

    Creates a dataset based on the filter_list combination
    which had the max percentual death change between a year and last,
    for all years in the df_mortality dataframe.

    For example, if filter_list = ["intent","sex"],
    max_death_change.get(2008) will return a dataframe in which
    the intent and sex combination of each row is the combination
    that caused the greater deaths change percentual between 2007
    and 2008, for the choosen county or state, depending on the map_scale
    parameter.

    Args:
        filter_list ([str]): df_mortality column names to filter for
        map_scale  (str): level of detail, for state level:  "state"
                                           for county level: "county_fips"

    Returns:
        map_scale: {year:dataframe}

    """
    filter_opts = filtering.no_filter(df_mortality)
    if map_scale == "county_fips":
        filter_opts = filtering.filter_state(df_mortality, filter_opts, state)
    df = df_mortality[filter_opts]

    df = df[["year",map_scale,"deaths"]+filter_list]
    df = df.groupby(["year",map_scale]+filter_list,as_index=False).sum()

    filter_empty = filtering.no_filter(df)
    max_death_change = {}
    for year in range(year_options_min+1,year_options_max+1):
        df_current = df[filtering.filter_year(df,filter_empty,year,year)]
        df_past = df[filtering.filter_year(df,filter_empty,year-1,year-1)]
        df_merge = pd.merge(df_past,df_current,on=[map_scale]+filter_list)[[map_scale,"deaths_x","deaths_y"]+filter_list]
        df_merge["deaths_change"] = ((df_merge["deaths_y"]-df_merge["deaths_x"])/df_merge["deaths_x"])
        idx = df_merge.groupby([map_scale])["deaths_change"].transform(max) == df_merge["deaths_change"]
        df_max = df_merge[idx]
        max_death_change.update({year:df_max})

    return max_death_change


def combined_report_fig(map_scale, year, filter_list,state):
    df = combined_report_data(map_scale, filter_list, state)
    df = df.get(year)

    hover_data = {"deaths_change":":.2%"}
    for f in filter_list:
        hover_data.update({f:True})

    return generate_map_fig(df,map_scale,hover_data)


# @cache.memoize()
def normal_map_data(map_scale, analytics_option,year,years_base,years_comparison,ages,cause,intent,ethnicity,sex,race,state):
    filter_opts = filtering.no_filter(df_mortality)
    # filter_opts = filtering.filter_age(df_mortality, filter_opts, ages[0], ages[1])
    filter_opts = filtering.filter_age_range(df_mortality, filter_opts, ages)
    filter_opts = filtering.filter_cause(df_mortality, filter_opts, cause)
    filter_opts = filtering.filter_intent(df_mortality, filter_opts, intent)
    filter_opts = filtering.filter_ethnicity(df_mortality, filter_opts, ethnicity)
    filter_opts = filtering.filter_sex(df_mortality, filter_opts, sex)
    filter_opts = filtering.filter_race(df_mortality, filter_opts, race)

    locations=map_scale if map_scale != 'regional' else 'state'
    if map_scale == "county_fips":
        filter_opts = filtering.filter_state(df_mortality, filter_opts, state)

    if analytics_option == "year_range":
        years_x = years_comparison
        years_y = years_base
    else:
        years_x = [year-1,year-1]
        years_y = [year,year]

    df_filtered = df_mortality[filter_opts]

    filter_opts = filtering.no_filter(df_filtered)
    filter_opts = filtering.filter_year(df_filtered, filter_opts, years_x[0], years_x[1])
    df_x = df_filtered[filter_opts]
    df_x = df_x.groupby(["year",locations],as_index=False).sum()[[locations,"deaths"]]
    df_x = df_x.groupby([locations],as_index=False).mean()[[locations,"deaths"]]

    filter_opts = filtering.no_filter(df_filtered)
    filter_opts = filtering.filter_year(df_filtered, filter_opts, years_y[0], years_y[1])
    df_y = df_filtered[filter_opts]
    df_y = df_y.groupby(["year",locations],as_index=False).sum()[[locations,"deaths"]]
    df_y = df_y.groupby([locations],as_index=False).mean()[[locations,"deaths"]]

    df = pd.merge(df_x,df_y,on=locations)
    df["deaths_change"] = ((df["deaths_y"]-df["deaths_x"])/df["deaths_x"])
    print(df)
    return df


def normal_map_fig(map_scale, analytics_option,year,years_base,years_comparison,ages,cause,intent,ethnicity,sex,race,state):
    df = normal_map_data(map_scale, analytics_option,year,years_base,years_comparison,ages,cause,intent,ethnicity,sex,race,state)
    hover_data = {"deaths_change":":.2%"}

    return generate_map_fig(df,map_scale,hover_data)

@app.callback(
     dash.dependencies.Output("Map", "figure"),
    [dash.dependencies.Input("map_scale", "value"),
     dash.dependencies.Input("analytics_option", "value"),
     dash.dependencies.Input("year", "value"),
     dash.dependencies.Input("years_base", "value"),
     dash.dependencies.Input("years_comparison", "value"),
     dash.dependencies.Input("Age", "value"),
     dash.dependencies.Input("Cause", "value"),
     dash.dependencies.Input("Intent", "value"),
     dash.dependencies.Input("Ethnicity", "value"),
     dash.dependencies.Input("Sex", "value"),
     dash.dependencies.Input("Race", "value"),
     dash.dependencies.Input("State", "value")]
)
def update_fig(map_scale, analytics_option,year,years_base,years_comparison,ages,cause,intent,ethnicity,sex,race,state):
    if analytics_option == "combined_report":
        return combined_report_fig(map_scale, year, ["intent"], state)
    else:
        return normal_map_fig(map_scale, analytics_option,year,years_base,years_comparison,ages,cause,intent,ethnicity,sex,race,state)
