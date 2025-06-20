# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

# Get min and max payload for RangeSlider
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Launch site options
launch_sites = [{'label': 'All Sites', 'value': 'ALL'}] + \
               [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]

# Create a Dash application
app = dash.Dash(__name__)

# Application layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Launch site dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=launch_sites,
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # Pie chart for launch success
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Range slider for payload
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={i: f'{i}' for i in range(0, 10001, 2500)},
        value=[min_payload, max_payload]
    ),

    # Scatter plot for payload vs. success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback for pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(site):
    if site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site',
                     title='Total Successful Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site]
        counts = filtered_df['class'].value_counts().reset_index()
        counts.columns = ['class', 'count']
        fig = px.pie(counts, values='count', names='class',
                     title=f'Success vs Failure for site {site}')
    return fig

# TASK 4: Callback for scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_plot(site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    filtered_df = spacex_df[mask]

    if site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == site]

    fig = px.scatter(
        filtered_df, x='Payload Mass (kg)', y='class',
        color='Booster Version Category',
        title=f'Payload vs. Success for {"All Sites" if site == "ALL" else site}'
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
