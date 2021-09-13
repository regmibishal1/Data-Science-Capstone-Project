# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', 
                                    options=[{'label': 'All Sites', 'value': 'ALL'}] + [{'label': i, 'value': i} for i in spacex_df['Launch Site'].unique()],
                                    value='ALL',
                                    placeholder='Select a Launch Site Here',
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000, value=[min_payload , max_payload],
                                    marks={
                                            0: '0 Kg',
                                            2500: '2500 Kg',
                                            5000: '5000 Kg',
                                            7500: '7500 Kg',
                                            10000: '10000 Kg'
                                        }),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))
def piechart(site):
    if site == 'ALL':
        data = spacex_df.groupby(['Launch Site']).sum().reset_index()
        figure = px.pie(data, values='class', names='Launch Site',
                        title='Total Success Launches by Site')
    else:
        data = spacex_df[spacex_df['Launch Site'] == site].groupby(['Launch Site','class']).count().reset_index()
        figure = px.pie(data, values='Flight Number', names='class',
                        title='Total Success Launches for Site {}'.format(site))

    return figure
    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value'))
def scatterplot(site, payload):
    low, high = payload
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    if site == 'ALL':
        figure = px.scatter(spacex_df[mask], x='Payload Mass (kg)', y='class', color="Booster Version Category", hover_data=['class'],
                            title='Correlation Between Payload and Success for all Site')

    else:
        data = spacex_df[spacex_df['Launch Site'] == site]
        figure = px.scatter(data[mask], x='Payload Mass (kg)', y='class', color="Booster Version Category", hover_data=['class'],
                            title='Correlation Between Payload and Success for Site {}'.format(site))
    return figure

# Run the app
if __name__ == '__main__':
    app.run_server()
