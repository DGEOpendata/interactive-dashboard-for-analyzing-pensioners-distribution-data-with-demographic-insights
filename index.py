python
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load data
data = pd.read_excel('Distribution_of_Pensioners_2022.xlsx')

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Pensioners Distribution Dashboard", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='quarter-dropdown',
        options=[
            {'label': f'Quarter {quarter}', 'value': quarter} for quarter in data['Quarter'].unique()
        ],
        placeholder="Select a Quarter"
    ),
    dcc.Graph(id='distribution-chart'),
    html.Div(id='summary-table')
])

# Callback for updating chart and table
@app.callback(
    [
        Output('distribution-chart', 'figure'),
        Output('summary-table', 'children')
    ],
    [Input('quarter-dropdown', 'value')]
)
def update_dashboard(selected_quarter):
    if not selected_quarter:
        return {}, "Please select a quarter to display data."

    filtered_data = data[data['Quarter'] == selected_quarter]

    # Create the chart
    figure = {
        'data': [
            {
                'x': filtered_data['Type'],
                'y': filtered_data['Count'],
                'type': 'bar',
                'name': 'Pensioners'
            }
        ],
        'layout': {
            'title': f'Distribution of Pensioners in Quarter {selected_quarter}'
        }
    }

    # Create the table
    table = html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in ['Type', 'Count', 'Percentage']])
        ),
        html.Tbody([
            html.Tr([
                html.Td(row['Type']), html.Td(row['Count']), html.Td(f"{row['Percentage']}%")
            ]) for index, row in filtered_data.iterrows()
        ])
    ])

    return figure, table

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
