# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[

    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
    ),

    # TASK 1: Dropdown
    dcc.Dropdown(
        id='id',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
        ],
        value='ALL',
        searchable=True
    ),

    html.Br(),

    # TASK 2: Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Range Slider
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={
            int(min_payload): str(int(min_payload)),
            int(max_payload): str(int(max_payload))
        },
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # TASK 4: Scatter plot
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2 callback (pie chart)
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('id', 'value')
)
def get_pie_chart(entered_site):

    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df,
            names='Launch Site',
            values='class',
            title='Total Successful Launches by Site'
        )
        return fig

    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]

        counts = filtered_df['class'].value_counts().reset_index()
        counts.columns = ['class', 'count']

        fig = px.pie(
            counts,
            names='class',
            values='count',
            title=f'Success vs Failure for {entered_site}'
        )
        return fig


# TASK 4 callback (scatter plot)
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('id', 'value'),
        Input('payload-slider', 'value')
    ]
)
def render_scatter(entered_site, payload_range):

    low, high = payload_range

    df_filtered = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if entered_site == 'ALL':

        fig = px.scatter(
            df_filtered,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs Success for All Sites'
        )
        return fig

    else:

        site_df = df_filtered[df_filtered['Launch Site'] == entered_site]

        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs Success for {entered_site}'
        )
        return fig


# Run the app
if __name__ == '__main__':
    app.run()