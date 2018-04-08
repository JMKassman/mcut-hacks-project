import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import requests
import pandas as pd

int_to_day = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

weekly_data = requests.get("https://www.purdue.edu/drsfacilityusage/api/WeeklyTrends").json()
locations = []
for element in weekly_data:
	if element['LocationName'] in locations:
		continue
	else:
		locations.append(element['LocationName'])

counts = {}
for location in locations:
	counts[location] = []
	for i in range(7):
		counts[location].append({})
		for j in range(24):
			counts[location][i][j] = 0

for element in weekly_data:
	counts[element['LocationName']][element['EntryDayOfWeek']][element['EntryHour']] = element['Count']

location_dicts = []
for location in locations:
	location_dicts.append({'label':location, 'value':location})

print(location_dicts)

app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(children='Corec Graph', style={'text-align':'center'}),
    dcc.Dropdown (
    	id='location-input',
    	options = location_dicts,
    	placeholder = 'Select Location',
    	multi = False
    ),
    dcc.Dropdown (
    	id='days',
        options = [
    		{'label': 'Sunday', 'value': 0},
    		{'label': 'Monday', 'value': 1},
    		{'label': 'Tuesday', 'value': 2},
    		{'label': 'Wednesday', 'value': 3},
    		{'label': 'Thursday', 'value': 4},
    		{'label': 'Friday', 'value': 5},
    		{'label': 'Saturday', 'value': 6}
    	],
    	placeholder = "Select Day(s)",
    	multi = True
    ),
    html.Div(id='output-graph')    
  ])


@app.callback(
  Output(component_id='output-graph', component_property='children'),
  [
  Input(component_id='location-input', component_property='value'),
  Input(component_id='days', component_property='value')
  ]
)
def update_graph(location, days):
  if location in locations:
    # location exists, draw graph
    d = {}
    for day in days:
      hour_data = []
      for i in range(24):
        hour_data.append(counts[location][day][i])
      d[day] = hour_data
    df = pd.DataFrame(data=d)
    data = []
    for day in df:
      data.append({
        'x': df.index,
        'y': df[day],
        'type': 'line',
        'name': int_to_day[day]
      })
    return dcc.Graph(
      id='graph',
      figure={
        'data': data,
        'layout': {
          'title': location
        }
      }
    )
  else:
    #location does not exist, tell user
    return html.P('Location Not Found')


if __name__ == "__main__":
  app.run_server(debug=False)
