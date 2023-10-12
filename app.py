import time
import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash import dash_table
from PIL import Image

app = Dash(__name__)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Read dataframe
df1 = pd.read_excel('user1.xlsx')
df2 = pd.read_excel('user2.xlsx')
df3 = pd.read_excel('user3.xlsx')

# Convert specific columns to numeric
numeric_columns = ["Weight & Body Mass (kg)", "Blood Oxygen Saturation (%)", "Active Energy (kJ)", "Basal Energy Burned (kJ)", "Exercise Time (min)"]

for df in [df1, df2, df3]:
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Coerce non-numeric values to NaN

# Using Pillow to read the images
pil_img1 = Image.open("user1.png")
pil_img2 = Image.open("user2.png")
pil_img3 = Image.open("user3.png")

# user 1 table
table_header1 = [
    html.Thead(html.Tr([html.Th("Name"), html.Td("Alice"), html.Th("Age"), html.Td("24")]))
]
row1 = html.Tr([html.Th("Sex"), html.Td("Female"), html.Th("Height (cm)"), html.Td("164.8")])
row2 = html.Tr([html.Th("Start date"), html.Td("1/9/22"), html.Th("End date"), html.Td("1/1/23")])
row3 = html.Tr([html.Th("Initial weight(kg)"), html.Td("75.4"), html.Th("Target weight(kg)"), html.Td("67")])
row4 = html.Tr([html.Th("Initial BMI level"), html.Td("overweight"), html.Th("Target BMI"), html.Td("Normal weight")])

table_body1 = [html.Tbody([row1, row2, row3, row4])]

# user 2 table
table_header2 = [
    html.Thead(html.Tr([html.Th("Name"), html.Td("Amy"), html.Th("Age"), html.Td('29')]))
]
row5 = html.Tr([html.Th("Sex"), html.Td("Female"), html.Th("Height (cm)"), html.Td("172.3")])
row6 = html.Tr([html.Th("Start date"), html.Td("27/12/21"), html.Th("End date"), html.Td("24/12/24")])
row7 = html.Tr([html.Th("Initial Weight(kg)"), html.Td('104.8'), html.Th("Target weight(kg)"), html.Td("80")])
row8 = html.Tr([html.Th("initial BMI"), html.Td("obesity level 2"), html.Th("Target BMI"), html.Td("overweight")])

table_body2 = [html.Tbody([row5, row6, row7, row8])]

# user 3 table
table_header3 = [
    html.Thead(html.Tr([html.Th("Name"), html.Td("Arthur"), html.Th("Age"), html.Td("32")]))
]

row9 = html.Tr([html.Th("Sex"), html.Td("Male"), html.Th("Height (cm)"), html.Td("178")])
row10 = html.Tr([html.Th("Start date"), html.Td("17/9/22"), html.Th("End date"), html.Td("17/12/22")])
row11 = html.Tr([html.Th("Initial Weight(kg)"), html.Td("105.2"), html.Th("Target Weight(kg)"), html.Td("98.9")])
row12 = html.Tr([html.Th("Initial BMI"), html.Td("obesity level 1"), html.Th("Target BMI"), html.Td("obesity level 1")])

table_body3 = [html.Tbody([row9, row10, row11, row12])]

# table for obesity level
df4 = pd.DataFrame({
    'Level': ['Normal Weight', 'Overweight', 'Obesity level I', 'Obesity level II', 'Obesity level III'],
    'BMI': ['19-24.9', '25-29.9', '30.0-34.9', '35-39.9', '≥ 40'],
    'Workout source': ['Roberta Gym', 'Roberta Gym', 'Roverta Gym', 'Roberta Gym', 'Roverta Gym'],
    'Link(s)': [
        '[Level 1](https://www.youtube.com/watch?v=C5P_9uzj1Cs&list=PLndmDqg0p2P5lTr8mylTpAanqmliEJ9-9&index=31)',
        '[Level 2](https://www.youtube.com/watch?v=WpIcrzTI2SA&list=PLndmDqg0p2P5lTr8mylTpAanqmliEJ9-9&index=32)',
        '[Level 3](https://www.youtube.com/watch?v=CB4U-0ZyjDI&list=PLndmDqg0p2P5lTr8mylTpAanqmliEJ9-9&index=36)',
        '[Level 4](https://www.youtube.com/watch?v=CB4U-0ZyjDI&list=PLndmDqg0p2P5lTr8mylTpAanqmliEJ9-9&index=36)',
        '[Level 5](https://www.youtube.com/watch?v=CB4U-0ZyjDI&list=PLndmDqg0p2P5lTr8mylTpAanqmliEJ9-9&index=36)']
})

# app layout
app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Weight Loss Tracker Dashboard"),
        html.Hr(),

        html.Br(),

        dbc.Tabs(
            [dbc.Tab(label="user1", tab_id="scatter"),
             dbc.Tab(label="user2", tab_id="histogram"),
             dbc.Tab(label="user3", tab_id="histogram1"),
             ],
            id="tabs",
            active_tab="scatter",
        ),

        html.Br(),
        dbc.Button(
            "Update the charts",
            color="primary",
            id="button",
            className="mb-3",
        ),

        # button with user information
        html.Div(id="tab-content", className="p-4"),
        # BMI calculator
        html.H3("BMI calculator"),
        html.Br(),
        html.Div(["Your Weight / kg: ", dcc.Input(id="user_weight", value=0, type='number')]),
        html.Div(["Your Height / cm: ", dcc.Input(id="user_height", value=0, type='number')]),
        html.Br(),
        html.Div(id='user_BMI'),

        # Dashtable
        html.H4("Exercise Level Evaluation"),
        dash_table.DataTable(data=df4.to_dict(orient='records'),
                             columns=[{'id': x, 'name': x, 'presentation': 'markdown'} if x == 'Link(s)' else {'id': x,
                                                                                                               'name': x}
                                      for x in df4.columns],
                             style_table={'position': 'relative', 'top': '5vh', 'left': '5vw', 'width': '60vw',
                                          'vertical-align': 'middle'}
                             ),
        html.Br(),
        html.Br(),
        html.Br(),

        # feedback for the clients
        html.Div([html.H5("Personal Note Space"),
                  dcc.Textarea(
                      id='textarea-example',
                      value='The comments to my users...',
                      style={'width': '50%', 'height': 150},
                  ),
                  html.Div(id='textarea-example-output', style={'whiteSpace': 'pre-line'})])

    ]
)


@app.callback(
    Output(component_id='user_BMI', component_property='children'),
    inputs=dict(a=Input('user_weight', 'value'), b=Input('user_height', 'value'))
)
def callback(a, b):
    if a and b is None:
        BMI = ''
    if a and b is not None:
        try:
            BMI = round(a / (b / 100) ** 2, 2)
        except ZeroDivisionError:
            BMI = 0
        return f'Current BMI: {BMI}'


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab, data):
    if active_tab and data is not None:
        if active_tab == "scatter":
            return dbc.Row(
                [
                    dbc.CardImg(src=pil_img1, style={'height': '10%', 'width': '10%', 'vertical-align': 'super'}),
                    dbc.CardBody(html.P("Progress bar", className="card-text")),
                    dbc.Progress(label='46%', value=46),
                    dbc.Col(dcc.Graph(figure=data["fig1"]), width=50),
                    dbc.Col(dcc.Graph(figure=data["fig4"]), width=50),
                    dbc.Col(dcc.Graph(figure=data["fig7"])),
                    dbc.Col(dcc.Graph(figure=data["fig10"])),
                    dbc.Table(table_header1 + table_body1, bordered=True),

                ])
        if active_tab == "histogram":
            return dbc.Row([
                dbc.CardImg(src=pil_img2, style={'height': '10%', 'width': '10%', 'vertical-align': 'super'}),
                dbc.CardBody(html.P("Progress bar", className="card-text")),
                dbc.Progress(label="92%", value=92),
                dbc.Col(dcc.Graph(figure=data["fig2"]), width=50),
                dbc.Col(dcc.Graph(figure=data["fig5"]), width=50),
                dbc.Col(dcc.Graph(figure=data["fig8"])),
                dbc.Col(dcc.Graph(figure=data["fig11"])),
                dbc.Table(table_header2 + table_body2, bordered=True)]),
        elif active_tab == "histogram1":
            return dbc.Row(
                [
                    dbc.CardImg(src=pil_img3, style={'height': '10%', 'width': '10%', 'vertical-align': 'super'}),
                    dbc.CardBody(html.P("Progress bar", className="card-text")),
                    dbc.Progress(label="38%", value=38),
                    dbc.Col(dcc.Graph(figure=data["fig3"]), width=50),
                    dbc.Col(dcc.Graph(figure=data["fig6"]), width=50),
                    dbc.Col(dcc.Graph(figure=data["fig9"])),
                    dbc.Col(dcc.Graph(figure=data["fig12"])),
                    dbc.Table(table_header3 + table_body3, bordered=True),
                ]
            )
    return "No tab selected"


@app.callback(
    Output('textarea-example-output', 'children'),
    Input('textarea-example', 'value')
)
def update_output(value):
    return 'Feedback for the clients: \n{}'.format(value)


@app.callback(Output("store", "data"), [Input("button", "n_clicks")])
def generate_graphs(n):
    if not n:
        # generate empty graphs when app loads
        return {k: go.Figure(data=[]) for k in
                ["fig1", "fig2", 'fig3', "fig4", 'fig5', 'fig6', "fig7", "fig8", 'fig9', "fig10", 'fig11', 'fig12', ]}

    time.sleep(2)

    # changing of weight
    # Changing of weight
    fig1 = px.line(df1, x="Date", y=["Weight & Body Mass (kg)", "Blood Oxygen Saturation (%)"],
                   title='Changing of Blood Oxygen Saturation(%) and weight')
    fig2 = px.line(df2, x="Date", y=["Weight & Body Mass (kg)", "Blood Oxygen Saturation (%)"],
                   title='Changing of Blood Oxygen Saturation(%) and weight')
    fig3 = px.line(df3, x="Date", y=["Weight & Body Mass (kg)", "Blood Oxygen Saturation (%)"],
                   title='Changing of Blood Oxygen Saturation(%) and weight')

    # 'Changing of Active Energy (kJ) and Basal Energy Burned (kJ)'
    fig4 = px.bar(df1.tail(30), x="Date", y=["Active Energy (kJ)", "Basal Energy Burned (kJ)"],
                  title='Active Energy & Basal Energy Burned(Last 30 Days)', labels={'value': 'Kilojoule (KJ)'})
    fig5 = px.bar(df2.tail(30), x="Date", y=["Active Energy (kJ)", "Basal Energy Burned (kJ)"],
                  title='Active Energy & Basal Energy Burned(Last 30 Days)', labels={'value': 'Kilojoule (KJ)'})
    fig6 = px.bar(df3.tail(30), x="Date", y=["Active Energy (kJ)", "Basal Energy Burned (kJ)"],
                  title='Active Energy & Basal Energy Burned(Last 30 Days)', labels={'value': 'Kilojoule (KJ)'})

    # Average Sleep time by Month
    fig7 = px.box(df1, x='Week', y='Sleep Analysis [In Bed] (hr)', title='Average Sleep Time by Week')
    fig8 = px.box(df2, x='Month', y='Sleep Analysis [In Bed] (hr)', title='Average Sleep Time by Month')
    fig9 = px.box(df3, x='Week', y='Sleep Analysis [In Bed] (hr)', title='Average Sleep Time by Week')

    # 'Exercise'
    fig10 = px.bar(data_frame=df1.groupby(['Week']).mean().reset_index(), y="Week", x="Exercise Time (min)",
                   orientation='h', title='Average Exercise Time by Week')
    fig11 = px.bar(data_frame=df2.groupby(['Month']).mean().reset_index(), y="Month", x="Exercise Time (min)",
                   orientation='h', title='Average Exercise Time by Month')
    fig12 = px.bar(data_frame=df3.groupby(['Week']).mean().reset_index(), y="Week", x="Exercise Time (min)",
                   orientation='h', title='Average Exercise Time by Week')

    # save figures in a dictionary for sending to the dcc.Store
    return {"fig1": fig1, "fig2": fig2, "fig3": fig3, "fig4": fig4, "fig5": fig5, "fig6": fig6, "fig7": fig7,
            "fig8": fig8, "fig9": fig9, "fig10": fig10, "fig11": fig11, "fig12": fig12}
for df in [df1, df2, df3]:
    print(f"Unique values in 'Date' column in DataFrame: {df['Date'].unique()}")
if __name__ == "__main__":
    app.run_server(debug=True)

