import base64
import datetime
import io
import os
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from app import app
from common.header import header_layout

import pandas as pd

import shutil

import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

flash_message = "" # Nothing when the page loads up.
flash_message_layout = html.Div([
    html.H2(flash_message),
], style={
    'borderRadius': '5px',
    'textAlign': 'center',
    'margin': '10px',
    'height': '30px',
    'display': 'none',
}, id='flash_message'
)

layout = html.Div([
    header_layout,
    flash_message_layout,
    dcc.RadioItems(
        options=[
            {'label': 'Append', 'value': 'append'},
            {'label': 'Overwrite(a backup will be saved)', 'value': 'overwrite'},
        ],
        value='append',
        style={
            'margin': 'auto',
            'textAlign': 'center'
        },
        id='upload-radio-button'
    ),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '60%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': 'auto'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    html.Div(id='output-data-upload'),
],
style={
    'margin': 'auto'
})


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            return "File processed successfully", df
        else:
            return "File type should be csv", ""

    except Exception as e:
        print(e)
        return f"Error: {e}", ""


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              Input('upload-radio-button', 'value'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, radio_button_selected, list_of_names, list_of_dates):
    if list_of_contents is not None:
        if radio_button_selected == 'append':
            existing_file_path = os.path.join(os.getcwd(), 'data', 'MortalityData_2001_2018_Final_v2.csv')
            columns = ['year','state','county','age','sex','race','ethnicity','cause','intent','deaths']
            if not os.path.exists(existing_file_path):
                df = pd.DataFrame(columns=columns)
                df.to_csv(existing_file_path, index=False)
            df = pd.read_csv(existing_file_path)
            status, uploaded_file = parse_contents(list_of_contents, list_of_names, list_of_dates)
            if uploaded_file is None:
                flash_message = status
                return html.H6(flash_message)
            if set(columns).issubset(uploaded_file.columns):
                df = pd.concat([df, uploaded_file])
            else:
                return html.h6("Column mismatch in the uploaded file!")
            df.to_csv(existing_file_path, index=False)

        if radio_button_selected == 'overwrite':
            # Save a backup first
            existing_file_path = os.path.join(os.getcwd(), 'data', 'MortalityData_2001_2018_Final_v2.csv')
            backup_path = os.path.join(os.getcwd(), 'data', 'backup', f'MortalityData_2001_2018_Final_v2_{datetime.datetime.now()}.csv')
            columns = ['year', 'state', 'county', 'age', 'sex', 'race', 'ethnicity', 'cause', 'intent', 'deaths']
            status, uploaded_file = parse_contents(list_of_contents, list_of_names, list_of_dates)
            if uploaded_file is None:
                flash_message = status
                return html.H6(flash_message)
            if set(columns).issubset(uploaded_file.columns):
                uploaded_file.drop(uploaded_file.columns.difference(columns), 1, inplace=True)
            else:
                return html.h6("Column mismatch in the uploaded file!")

            if os.path.exists(existing_file_path):
                shutil.move(existing_file_path, backup_path)
            uploaded_file.to_csv(existing_file_path, index=False)
        else:
            pass
        #
        # children = [
        #     parse_contents(c, n, d) for c, n, d in
        #     zip(list_of_contents, list_of_names, list_of_dates)]
        return html.H6("Data uploaded")
