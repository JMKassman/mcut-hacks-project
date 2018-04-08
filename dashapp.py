import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import requests

weekly_data = requests.get("https://www.purdue.edu/drsfacilityusage/api/WeeklyTrends").json()



app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(children='Corec Graph'),
    dcc.Input(id='location_input', value='', type='text'),
    dcc.Dropdown (
    	options = [
    		{'label': 'Sunday', 'value': 0},
    		{'label': 'Monday', 'value': 1},
    		{'label': 'Tuesday', 'value': 2},
    		{'label': 'Wednesday', 'value': 3},
    		{'label': 'Thursday', 'value': 4},
    		{'label': 'Friday', 'value': 5},
    		{'label': 'Saturday', 'value': 6}
    	],
    	multi = True,
    	value = 0
    )
  ])

if __name__ == "__main__":
  app.run_server(debug=True)
