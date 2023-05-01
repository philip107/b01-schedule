import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Read in data from CSV


df = pd.read_csv('employee_schedule.csv')

# Create dropdown options for employees, departments, and restaurants
employee_options = [{'label': 'All Employees', 'value': 'All'}] + [{'label': i, 'value': i} for i in df['Employee'].unique()]
department_options = [{'label': 'All Departments', 'value': 'All'}] + [{'label': i, 'value': i} for i in df['Department'].unique()]
restaurant_options = [{'label': 'All Restaurants', 'value': 'All'}] + [{'label': i, 'value': i} for i in df['Restaurant Short Name'].unique()]

# Create Dash app
app = dash.Dash(__name__)

server = app.server

# Define app layout
app.layout = html.Div(children=[
    html.H1(children='Employee Schedule'),

    html.Div(children='''
        Select a department to view schedules:
    '''),

    dcc.Dropdown(
        id='department-dropdown',
        options=department_options,
        value='All'
    ),

    html.Div(children='''
        Select an employee to view their schedule:
    '''),

    dcc.Dropdown(
        id='employee-dropdown',
        options=employee_options,
        value='All'
    ),
    
    html.Div(children='''
        Select a restaurant to view schedules:
    '''),

    dcc.Dropdown(
        id='restaurant-dropdown',
        options=restaurant_options,
        value='All'
    ),

    dcc.Graph(
        id='schedule-plot'
    )
])

# Define callback to update schedule plot based on department, employee, and restaurant dropdowns
@app.callback(
    Output('schedule-plot', 'figure'),
    Input('department-dropdown', 'value'),
    Input('employee-dropdown', 'value'),
    Input('restaurant-dropdown', 'value'))
def update_schedule(department, employee, restaurant):
    if department == 'All':
        if employee == 'All':
            if restaurant == 'All':
                filtered_df = df
                title = 'All Employees Schedule for All Restaurants Across All Departments'
            else:
                filtered_df = df[df['Restaurant Short Name'] == restaurant]
                title = 'All Employees Schedule for {} Across All Departments'.format(restaurant)
        elif restaurant == 'All':
            filtered_df = df[df['Employee'] == employee]
            title = 'Schedule for {} Across All Departments for All Restaurants'.format(employee)
        else:
            filtered_df = df[(df['Employee'] == employee) & (df['Restaurant Short Name'] == restaurant)]
            title = 'Schedule for {} Across All Departments for {}'.format(employee, restaurant)
    elif employee == 'All':
        if restaurant == 'All':
            filtered_df = df[df['Department'] == department]
            title = '{} Schedule for All Employees Across All Restaurants'.format(department)
        else:
            filtered_df = df[(df['Department'] == department) & (df['Restaurant Short Name'] == restaurant)]
            title = '{} Schedule for All Employees for {}'.format(department, restaurant)
    elif restaurant == 'All':
        filtered_df = df[(df['Department'] == department) & (df['Employee'] == employee)]
        title = '{} Schedule for {}'.format(employee, department)
    else:
        filtered_df = df[(df['Department'] == department) & (df['Employee'] == employee) & (df['Restaurant Short Name'] == restaurant)]
        title = '{} Schedule for {} at {}'.format(employee, department, restaurant)
        
    fig = px.timeline(filtered_df, x_start='Start Time', x_end='End Time', y='Employee', color='Task')
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Employee',
        title=title
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)