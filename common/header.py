import dash_html_components as html
import dash_core_components as dcc

header_layout = html.Div([
	html.H1(children="Fatal Injury and Violence Analytics"),
	html.Div([
		html.Div([
			dcc.Link('Metric vs time dashboard view', href='/apps/metric-vs-time-view'),
		], className="two columns"),
		html.Div([
			dcc.Link('Map view', href='/apps/map-view'),
		], className="two columns"),
		html.Div([
			dcc.Link('Table view', href='/apps/table-view'),
		], className="two columns"),
		html.Div([
			dcc.Link('Data upload view', href='/apps/data-upload-view'),
		], className="two columns"),
	], className="row"),
])
