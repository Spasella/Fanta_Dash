import pandas as pd
import pandasql as ps
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import Dash, dcc, html, Input, Output, State, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots
import plotly.subplots as sp
import dash_ag_grid as dag
import plotly.io as pio
import numpy as np
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import webbrowser
from threading import Timer





#_________DATASOURCE___________


source = pd.read_csv('https://raw.githubusercontent.com/Spasella/Fantadash-/main/Fantadash_dataset%20-%202021-2022-2023%20(3).csv',
                        low_memory=False)

#source = pd.read_csv("Fantadash_dataset - 2021-2022-2023 (3).csv")


source["Giornata_Match"] = source["Giornata"].astype(str) + " " + source["Partita"].astype(str)

#__________ELEMENTS_____________

#Style
color_red = "#a70a2d"
color_blue = "#0f2537"



#Tabs Offcanvas
tabs = dbc.Tabs([

        # AGGIUNGI NUOVI RECORD
        dbc.Tab(dbc.Card([
        dbc.CardBody([

            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Add csv o ',
                    html.A('Select File')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.Div(id='output-data-upload'),
        ]),
        dbc.CardFooter(
            dbc.Button(id='_add_record_button_', children="Aggiungi", color="primary", className="me-1")
        )
    ], className="mb-3"),
                        label="Create Team" ,
                        tab_id="tab-aggiungi",
                        className="nav nav-tabs",

                        active_label_style={"color": color_red,
                                            "bg-color": color_blue},

                        label_style={"border-color": color_blue,
                                     'border-radius': '3px',
                                     "font-size": "15px",
                                     'font-weight': 'bold'}),
        html.Br(),
        #MODIFICA IL RECORD
        dbc.Tab(dbc.Card([
                    dbc.CardBody([
                        dbc.Input(id='_mdfc_cdfs_input_', type="text", placeholder="Add a Team Name"),
                        html.Br(),
                        dbc.Input(id='_mdfc_clnn_input_', type="text", placeholder="Add Players"),
                        html.Br(),
                        dbc.Input(id='_mdfc_nvlr_input_', type="text", placeholder="Add something funny but not stupid")
                    ]),
                    dbc.CardFooter(
                        dbc.Button(id='_mdfc_submit_button_', children="Modifica", color="primary", className="me-1")
                    ),
                    html.Div(id="_mdfc_cdfs_output_"),
                    html.Div(id="_mdfc_clnn_output_"),
                    html.Div(id="_mdfc_nvlr_output_"),

                ], className="mb-3"),
                                    label="Modify Team",
                                    tab_id="tab-modifica",
                                    className="nav nav-tabs",
                                    active_label_style={"color": color_red,
                                                        "bg-color": color_blue},

                                    label_style={"border-color": color_blue,
                                                 'border-radius': '1px',
                                                 "font-size": "15px",
                                                 'font-weight': 'bold'})
    ,
        html.Br(),
        # ELIMINA IL RECORD
        dbc.Tab(dbc.Card([
                dbc.CardBody([
                    dbc.Input(id='_delete_cdfs_input_', type="text", placeholder="Add Team Name"),
                ]),
                dbc.CardFooter(
                    dbc.Button(id='_delete_submit_button_', children="Elimina", color="primary", className="me-1")
                ),
                html.Div(id="_delete_cdfs_output_")

        ], className="mb-3"),
                              label="Elimina",
                              tab_id="tab-elimina",
                              className="nav nav-tabs",

                              active_label_style={"color": color_red,
                                                  "bg-color": color_blue},

                              label_style={"border-color":color_blue,
                                           'border-radius': '1px',
                                           "font-size":"15px",
                                           'font-weight': 'bold'}),


], id="tabs", active_tab="tab-modifica")

#Offcanvas
offcanvas = html.Div([
        dbc.Button("☰", id="open-offcanvas", n_clicks=0, color="black", style={"float": "left"}),

        dbc.Offcanvas(tabs,
            id="offcanvas",
            title="COMING SOON",
            is_open=False,
            style={"bg-color": "darkviolet",
                   "color": "white",
                   'width': 400}
        ),
    ])




#Tab Offcanvas Fantabot
tab_fantabot = html.Div([

    dbc.Textarea(id='input_api_key', placeholder="Insert key", style={"height": "50px"}),
    html.Br(),
    dbc.Textarea(id='input_fantabot', placeholder="Write something...", style={"height": "200px"}),
    html.Br(),
    dbc.Button(id='submit_prompt_fantabot', children="Submit", color="darkviolet", className="me-1",
               style={"color": "darkviolet", "border": "1px solid darkviolet", "marginLeft": "480px"}),
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Spinner(html.Div(id="loading-output"), color="darkviolet", type="grow"),
    dbc.Textarea(id="output_fantabot")
])


#Offcanvas FantaBot
offcanvas_fantabot = html.Div([
        dbc.Button("FantaBot!", id="open-offcanvas-fantabot", n_clicks=0, color="black", style={"float": "right"}),

        dbc.Offcanvas(
            tab_fantabot,
            id="offcanvas-fantabot",
            title="FantaBot!\n__________________________________________________",
            is_open=False,
            style={"bg-color": "darkviolet",
                   "color": "white",
                   'width': 600}
        ),
    ])





#Navbar
navbar = dbc.Navbar([
    dbc.Row(
        [

            dbc.Col(html.Div(id="Hidden Column1")),

            dbc.Col(html.Div(id="Hidden Column2")),

            dbc.Col(html.Div(id="Hidden Column3")),

            dbc.Col(html.Div([offcanvas]),
                    style={
                        "color": "white",
                        "border": "1px solid darkviolet",
                        "backgroundColor": "darkviolet",
                    },
            ),

            dbc.Col(
                dcc.Dropdown(
                    id="player1-dropdown",
                    options=[{"label": option, "value": option} for option in source["Giocatori"].unique()],
                    placeholder="Player 1",
                    className="mr-3",
                    value="Onana",
                    style={
                        "width": "200px",
                        "marginRight": "5px",
                        "backgroundColor": "black",
                        "color": "darkviolet",
                        "border": "1px solid darkviolet",
                    },
                ),

            ),

            dbc.Col(
                dcc.Dropdown(
                    id="team-dropdown",
                    options=[
                        {"label": option, "value": option}
                        for option in source["Squadra"].unique()
                    ],
                    placeholder="Team",
                    className="mr-3",
                    style={
                        "width": "200px",
                        "marginRight": "5px",
                        "backgroundColor": "black",
                        "color": "darkviolet",
                        "border": "1px solid darkviolet",
                    },
                ),

            ),

            dbc.Col(
                dcc.Dropdown(
                    id="role-dropdown",
                    options=[
                        {"label": option, "value": option}
                        for option in source["Ruolo"].unique()
                    ],
                    placeholder="Role",
                    className="mr-3",
                    style={
                        "width": "200px",
                        "marginRight": "5px",
                        "backgroundColor": "black",
                        "color": "darkviolet",
                        "border": "1px solid darkviolet",
                    },
                ),

            ),

            dbc.Col(
                dcc.Dropdown(
                    id="season-dropdown",
                    options=[
                        {"label": option, "value": option}
                        for option in source["stagione_partita"].unique()
                    ],
                    placeholder="Season",
                    className="mr-3",
                    value="2022-2023",
                    style={
                        "width": "200px",
                        "marginRight": "5px",
                        "backgroundColor": "black",
                        "color": "darkviolet",
                        "border": "1px solid darkviolet",
                    },
                ),

            ),

            dbc.Col(
                dcc.Dropdown(
                    id="player2-dropdown",
                    options=[
                        {"label": option, "value": option}
                        for option in source["Giocatori"].unique()
                    ],
                    placeholder="Player 2",
                    className="mr-3",
                    value="Ochoa",
                    style={
                        "width": "200px",
                        "marginRight": "5px",
                        "backgroundColor": "black",
                        "color": "darkviolet",
                        "border": "1px solid darkviolet",
                    },
                ),

            ),

            dbc.Col(html.Div([offcanvas_fantabot]),
                    style={
                        "color": "white",
                        "border": "1px solid darkviolet",
                        "backgroundColor": "darkviolet",
                    },

            ),

        ],
        justify="between",
    )
], color="black", dark=True, sticky="top", style={"height": "60px", "width": "100%", "border": "1px solid darkviolet"})


#Card Pre, Amm, Esp
card_players = dbc.Row([

            #Presenze Player 1
            dbc.Col([dbc.Card([
                dbc.CardBody(
                    [
                        html.Div(f"PRESENCES", className="card-header"),
                        html.Div(className="card-title", id="presenze_giocatore1"),
                    ]
                            ),
                    ], className="card border-success mb-3")
                    ],xl=2, lg=2, md=2, sm=2, xs=2),

            #Ammonizioni Player 1
            dbc.Col([dbc.Card([
                dbc.CardBody(
                    [
                        html.Div(f"PENALTIES", className="card-header"),
                        html.H4(f"{11}", className="card-title", id="ammonizioni_giocatore1"),
                    ]
                ),
            ], className="card border-warning mb-3")
            ], xl=2, lg=2, md=2, sm=2, xs=2),


            #Espulsioni Player 1
            dbc.Col([dbc.Card([
                dbc.CardBody(
                    [
                        html.Div(f"EXPULSIONS", className="card-header"),
                        html.H4(f"{2}", className="card-title", id="espulsioni_giocatore1"),
                    ]
                ),
            ], className="card border-danger mb-3")
            ], xl=2, lg=2, md=2, sm=2, xs=2),

            # Presenze Player 2
            dbc.Col([dbc.Card([
                dbc.CardBody(
                    [
                        html.Div(f"PRESENCES", className="card-header"),
                        html.H4(f"{12}", className="card-title", id="presenze_giocatore2"),
                    ]
                ),
            ], className="card border-success mb-3")
            ], xl=2, lg=2, md=2, sm=2, xs=2),

            # Ammonizioni Player 2
            dbc.Col([dbc.Card([
                dbc.CardBody(
                    [
                        html.Div(f"PENALTIES", className="card-header"),
                        html.H4(f"{12}", className="card-title", id="ammonizioni_giocatore2"),
                    ]
                ),
            ], className="card border-warning mb-3")
            ], xl=2, lg=2, md=2, sm=2, xs=2),

            # Espulsioni Player 2
            dbc.Col([dbc.Card([
                dbc.CardBody(
                    [
                        html.Div(f"EXPULSIONS", className="card-header"),
                        html.H4(f"{34}", className="card-title", id="espulsioni_giocatore2"),
                    ]
                ),
            ], className="card border-danger mb-3")
            ], xl=2, lg=2, md=2, sm=2, xs=2),



    ])


#Stats Player: goal_fatti_tot, goal_subiti_tot, assist_tot,
#              rigori_segnati_tot, rigori_sbagliati_tot, rigori_parati_tot, autoreti_tot

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

stats_p1 = dbc.Row([

    #goal_fatti_tot Player 1
    dbc.Col(dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.P("Goal", className="card-title"),
                    html.H4(f"{12}",id="goal_giocatore1" , className="card-text",),
                ],
                className="text-center"
            ),
            style={"height": "100px"}
        ),
        dbc.Card(
            html.Div(className="fa fa-list", style=card_icon),
            className="bg-success",
            style={"maxWidth": 10},
        ),
    ],
    className="mt-4 shadow",
), xl=2, lg=2, md=2, sm=2, xs=2),

    #assist_tot Player 1______________________________________
    dbc.Col(dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.P("Assist", className="card-title"),
                    html.H4(f"{2}",id="assist_giocatore1" , className="card-text",),
                ],
                className="text-center"
            ),
            style={"height": "100px"}
        ),
        dbc.Card(
            html.Div(className="fa fa-list", style=card_icon),
            className="bg-success",
            style={"maxWidth": 10},
        ),
    ],
    className="mt-4 shadow",
), xl=2, lg=2, md=2, sm=2, xs=2),


    # rigori_segnati_tot Player 1
    dbc.Col(dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.P("Rig.Seg.", className="card-title"),
                    html.H4(f"{2}",id="rigori_giocatore1" , className="card-text",),
                ],
                className="text-center"
            ),
            style={"height": "100px"}
        ),
        dbc.Card(
            html.Div(className="fa fa-list", style=card_icon),
            className="bg-success",
            style={"maxWidth": 10},
        ),
    ],
    className="mt-4 shadow",
), xl=2, lg=2, md=2, sm=2, xs=2),


    # rigori_parati_tot Player 1
    dbc.Col(dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.P("Rig.Par.", className="card-title"),
                    html.H4(f"{2}",id="rigoriparati_giocatore1" , className="card-text",),
                ],
                className="text-center"
            ),
            style={"height": "100px"}
        ),
        dbc.Card(
            html.Div(className="fa fa-list", style=card_icon),
            className="bg-success",
            style={"maxWidth": 10},
        ),
    ],
    className="mt-4 shadow",
), xl=2, lg=2, md=2, sm=2, xs=2),


    # goal_subiti_tot Player 1
    dbc.Col(dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.P("GoalSub.", className="card-title"),
                    html.H4(f"{2}",id="goalsubiti_giocatore1" , className="card-text",),
                ],
                className="text-center"
            ),
            style={"height": "100px"}
        ),
        dbc.Card(
            html.Div(className="fa fa-list", style=card_icon),
            className="bg-danger",
            style={"maxWidth": 10},
        ),
    ],
    className="mt-4 shadow",
), xl=2, lg=2, md=2, sm=2, xs=2),


    # autoreti_tot Player 1
    dbc.Col(dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.P("Autogoal", className="card-title"),
                    html.H4(f"{2}",id="autogoal_giocatore1" , className="card-text",),
                ],
                className="text-center"
            ),
            style={"height": "100px"}
        ),
        dbc.Card(
            html.Div(className="fa fa-list", style=card_icon),
            className="bg-danger",
            style={"maxWidth": 10},
        ),
    ],
    className="mt-4 shadow",
), xl=2, lg=2, md=2, sm=2, xs=2),



    ])
stats_p2 = dbc.Row([

    #goal_fatti_tot Player 2
    dbc.Col(dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.P("Goal", className="card-title"),
                    html.H4(f"{12}",id="goal_giocatore2" , className="card-text",),
                ],
                className="text-center"
            ),
            style={"height": "100px"}
        ),
        dbc.Card(
            html.Div(className="fa fa-list", style=card_icon),
            className="bg-success",
            style={"maxWidth": 10},
        ),
    ],
    className="mt-4 shadow",
), xl=2, lg=2, md=2, sm=2, xs=2),

    #assist_tot Player 2______________________________________
    dbc.Col(dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.P("Assist", className="card-title"),
                    html.H4(f"{2}",id="assist_giocatore2" , className="card-text",),
                ],
                className="text-center"
            ),
            style={"height": "100px"}
        ),
        dbc.Card(
            html.Div(className="fa fa-list", style=card_icon),
            className="bg-success",
            style={"maxWidth": 10},
        ),
    ],
    className="mt-4 shadow",
), xl=2, lg=2, md=2, sm=2, xs=2),


    # rigori_segnati_tot Player 2
    dbc.Col(dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.P("Rig.Seg.", className="card-title"),
                    html.H4(f"{2}",id="rigori_giocatore2" , className="card-text",),
                ],
                className="text-center"
            ),
            style={"height": "100px"}
        ),
        dbc.Card(
            html.Div(className="fa fa-list", style=card_icon),
            className="bg-success",
            style={"maxWidth": 10},
        ),
    ],
    className="mt-4 shadow",
), xl=2, lg=2, md=2, sm=2, xs=2),


    # rigori_parati_tot Player 2
    dbc.Col(dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.P("Rig.Par.", className="card-title"),
                    html.H4(f"{2}",id="rigoriparati_giocatore2" , className="card-text",),
                ],
                className="text-center"
            ),
            style={"height": "100px"}
        ),
        dbc.Card(
            html.Div(className="fa fa-list", style=card_icon),
            className="bg-success",
            style={"maxWidth": 10},
        ),
    ],
    className="mt-4 shadow",
), xl=2, lg=2, md=2, sm=2, xs=2),


    # goal_subiti_tot Player 2
    dbc.Col(dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.P("GoalSub.", className="card-title"),
                    html.H4(f"{2}",id="goalsubiti_giocatore2" , className="card-text",),
                ],
                className="text-center"
            ),
            style={"height": "100px"}
        ),
        dbc.Card(
            html.Div(className="fa fa-list", style=card_icon),
            className="bg-danger",
            style={"maxWidth": 10},
        ),
    ],
    className="mt-4 shadow",
), xl=2, lg=2, md=2, sm=2, xs=2),


    # autoreti_tot Player 2
    dbc.Col(dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.P("Autogoal", className="card-title"),
                    html.H4(f"{2}",id="autogoal_giocatore2" , className="card-text",),
                ],
                className="text-center"
            ),
            style={"height": "100px"}
        ),
        dbc.Card(
            html.Div(className="fa fa-list", style=card_icon),
            className="bg-danger",
            style={"maxWidth": 10},
        ),
    ],
    className="mt-4 shadow",
), xl=2, lg=2, md=2, sm=2, xs=2),



    ])






stats1_players1 = dbc.Row([

                    #goal_fatti_tot Player 1
                    dbc.Col([dbc.Card([
                        dbc.CardBody(
                            [
                                html.Div(f"Goal scored", className="card-header"),
                                html.H4(f"{10}", className="card-title", id="goal_giocatore1"),
                            ]
                                    ),
                            ], className="card border-danger mb-3", style={"width": "150px", "height": "120px"})
                            ],xl=1, lg=1, md=1, sm=1, xs=1),


                    #assist_tot Player 1
                    dbc.Col([dbc.Card([
                        dbc.CardBody(
                            [
                                html.Div(f"Assist", className="card-header"),
                                html.H4(f"{2}", className="card-title", id="assist_giocatore1"),
                            ]
                        ),
                    ], className="card border-danger mb-3", style={"width": "150px", "height": "120px"})
                    ], xl=1, lg=1, md=1, sm=1, xs=1),

                    # rigori_segnati_tot Player 1
                    dbc.Col([dbc.Card([
                        dbc.CardBody(
                            [
                                html.Div(f"Penalty kick", className="card-header"),
                                html.H6(f"{2}", className="card-title", id="rigori_giocatore1"),

                            ]
                        ),
                    ], className="card border-danger mb-3", style={"width": "150px", "height": "120px"})
                    ], xl=1, lg=1, md=1, sm=1, xs=1),

                    ])
stats2_players1 = dbc.Row([
                    # rigori_parati_tot Player 1
                    dbc.Col([dbc.Card([
                        dbc.CardBody(
                            [
                                html.Div(f"Penalty kick parati", className="card-header"),
                                html.H4(f"{2}", className="card-title", id="rigoriparati_giocatore1"),
                            ]
                        ),
                    ], className="card border-danger mb-3", style={"width": "150px", "height": "120px"})
                    ], xl=2, lg=2, md=2, sm=2, xs=2),

                    # goal_subiti_tot Player 1
                    dbc.Col([dbc.Card([
                        dbc.CardBody(
                            [
                                html.Div(f"Goals conceded", className="card-header"),
                                html.H4(f"{11}", className="card-title", id="goalsubiti_giocatore1"),
                            ]
                        ),
                    ], className="card border-danger mb-3", style={"width": "150px", "height": "120px"})
                    ], xl=2, lg=2, md=2, sm=2, xs=2),

                    # autoreti_tot Player 1
                    dbc.Col([dbc.Card([
                        dbc.CardBody(
                            [
                                html.Div(f"Autogoal", className="card-header"),
                                html.H4(f"{2}", className="card-title", id="autogoal_giocatore1"),
                            ]
                        ),
                    ], className="card border-danger mb-3", style={"width": "150px", "height": "120px"})
                    ], xl=2, lg=2, md=2, sm=2, xs=2),

])









#_____________APP________________


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server



app.layout = html.Div(
    style={
        "backgroundImage": "url('assets/2bg_neon.JPG')",
        "backgroundSize": "1500px 1200px",
        "background-position": "10px 50px",
        "backgroundRepeat": "no-repeat"
    },
    children=[
        html.Br(),
        html.Div([
            html.H1("FANTADASH!", style={"textAlign": "center", "color": "white",
                                         "fontFamily": "fantasy", "fontSize": "36px",
                                         "textDecorationColor": "white"},
                   ),
        ]),
        navbar,
        html.Div(style={"borderLeft": "1px solid white", "height": "200vh", "position": "absolute", "left": "50%"}),
        html.Br(),
        card_players,

        dbc.Row([
            dbc.Col([dcc.Graph(id= "gauge_p1"),
                     stats_p1,
                     html.Br(),
                     dcc.Graph(id="stats_giornate_p1"),
                     dcc.Graph(id="voti_giornate_p1")],
                    xs=6, xl= 6, xxl=6),
            dbc.Col([dcc.Graph(id= "gauge_p2"),
                     stats_p2,
                     html.Br(),
                     dcc.Graph(id="stats_giornate_p2"),
                     dcc.Graph(id="voti_giornate_p2")
                     ], xs=6, xl= 6, xxl=6)
                ]),


    ],
)










#                            ...CallBack Space...



#Offancav FantaBot! Callback
@app.callback(
    Output("offcanvas-fantabot", "is_open"),
    [Input("open-offcanvas-fantabot", "n_clicks")],
    [State("offcanvas-fantabot", "is_open")],
)
def toggle_offcanvas(n, is_open):
    if n:
        return not is_open
    return is_open

#_______________________________________________________________________

#ChatBot Callback

@app.callback(
    [Output('loading-output', 'children'),
     Output('output_fantabot', 'value')],
    [Input('submit_prompt_fantabot', 'n_clicks')],
    [State('input_fantabot', 'value'),
     State("input_api_key", "value"),
     State('output_fantabot', 'value')],
    prevent_initial_call=True
)
def update_output(n_clicks, input_value, api_key, output_state):
    if n_clicks and input_value and api_key:
        # Qui puoi iniziare a mostrare la barra di caricamento
        loading_child = "Caricamento..."

        # Salviamo l'input dell'utente in una variabile
        global saved_input

        saved_input = input_value

        #print(saved_input)


        #Prendiamo il dataset senza le partite, ma solo con le stats dei giocatori
        df = pd.read_csv("https://raw.githubusercontent.com/Spasella/Fantadash-/main/Fantabot_dataset%20-%202021-2022-2023%20(3).csv",
                         low_memory=False)

        # Convertiamo le colonne 'Media Voto' e 'Fanta Media' in float
        df['Media Voto'] = df['Media Voto'].astype(float)
        df['Fanta Media'] = df['Fanta Media'].astype(float)

        # Elenco delle colonne da convertire in int
        colonne_interi = ['Presenze', 'Goal Fatti', 'Goal Subiti', 'Rigori Parati', 'Rigori Calciati',
                          'Rigori Segnati', 'Rigori Sbagliati', 'Assist', 'Ammonizioni']

        # Convertiamo le colonne specificate in int
        for col in colonne_interi:
            df[col] = df[col].astype(int)

        #Richiamiamo il llm di OpenAI
        llm = OpenAI(api_token=api_key)

        #Innestiamolo in pandas_ai
        pandas_ai = PandasAI(llm, conversational=True)

        #Prendiamo il response
        response = pandas_ai(df, saved_input)

        #Restituiamolo all'utente
        print(response)
        return "", response

    else:
        return "", "Non hai scritto niente"



#________________________________________________________________


# Dropdown Callback

@app.callback(
    Output("player1-dropdown", "options"),
    Output("player2-dropdown", "options"),
    [Input("role-dropdown", "value"),
     Input("season-dropdown", "value"),
     Input("team-dropdown", "value")]
)
def update_player_dropdown(role, season, team):
    filtered_df = source
    if role:
        filtered_df = filtered_df[filtered_df["Ruolo"] == role]
    if season:
        filtered_df = filtered_df[filtered_df["stagione_partita"] == season]
    if team:
        filtered_df = filtered_df[filtered_df["Squadra"] == team]
    options = [{"label": option, "value": option} for option in filtered_df["Giocatori"].unique()]
    return options, options




# Offcanvas Callback
@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    State("offcanvas", "is_open"),
)
def toggle_offcanvas(open_offcanvas, is_open):
    if open_offcanvas:
        return not is_open
    return is_open


# Player Card Callback

#                   PLAYER 1

@app.callback(
    Output("presenze_giocatore1", "children"),
    Output("ammonizioni_giocatore1", "children"),
    Output("espulsioni_giocatore1", "children"),
    Output("goal_giocatore1", "children"),
    Output("assist_giocatore1", "children"),
    Output("rigori_giocatore1", "children"),
    Output("rigoriparati_giocatore1", "children"),
    Output("goalsubiti_giocatore1", "children"),
    Output("autogoal_giocatore1", "children"),
    Input("player1-dropdown", "value"),
    Input("season-dropdown", "value")
)

def pres_player1(player1, season):
    value = [player1]
    stag = [season]
    #print(value)
    #print("__________")
    # Filtriamo per il giocatore selezionato
    filtered_source = source[source["Giocatori"].isin(value)]
    filtered_source = filtered_source[filtered_source["stagione_partita"].isin(stag)]

    # Prendiamo la prima riga del dataset
    payer_details = filtered_source[0:1]
    #print(payer_details)

    # Prendiamo pres tot, amm tot, esp tot
    pre_player1 = payer_details["Presenze"].iloc[0]
    amm_player1 = payer_details["Ammonizioni"].iloc[0]
    esp_player1 = payer_details["Espulsioni"].iloc[0]

    #print("__________")
    #print(pre_player1, amm_player1, esp_player1)

    # Prendiamo goal_fatti_tot, assist_tot, rigori_segnati_tot, rigori_parati_tot,
    #           goal_subiti_tot, autoreti_tot

    goal_fatti_tot = payer_details["Goal Fatti"].iloc[0]
    assist_tot = payer_details["Assist"].iloc[0]
    rigori_segnati_tot = payer_details["Rigori Segnati"].iloc[0]
    rigori_parati_tot = payer_details["Rigori Parati"].iloc[0]
    goal_subiti_tot = payer_details["Goal Subiti"].iloc[0]
    autoreti_tot = payer_details["Autogoal"].iloc[0]


    return html.H4([f'{pre_player1}']), html.H4([f'{amm_player1}']), html.H4([f'{esp_player1}']), html.H4([f'{goal_fatti_tot}']), html.H4([f'{assist_tot}']), html.H4([f'{rigori_segnati_tot}']), html.H4([f'{rigori_parati_tot}']), html.H4([f'{goal_subiti_tot}']), html.H4([f'{autoreti_tot}'])


#                   PLAYER 2

@app.callback(
    Output("presenze_giocatore2", "children"),
    Output("ammonizioni_giocatore2", "children"),
    Output("espulsioni_giocatore2", "children"),
    Output("goal_giocatore2", "children"),
    Output("assist_giocatore2", "children"),
    Output("rigori_giocatore2", "children"),
    Output("rigoriparati_giocatore2", "children"),
    Output("goalsubiti_giocatore2", "children"),
    Output("autogoal_giocatore2", "children"),
    Input("player2-dropdown", "value"),
    Input("season-dropdown", "value")
)

def pres_player2(player2, season):
    value = [player2]
    stag = [season]
    #print(value)
    #print("__________")
    # Filtriamo per il giocatore selezionato
    filtered_source = source[source["Giocatori"].isin(value)]
    filtered_source = filtered_source[filtered_source["stagione_partita"].isin(stag)]

    # Prendiamo la prima riga del dataset
    payer_details = filtered_source[0:1]
    #print(payer_details)

    # Prendiamo pres tot, amm tot, esp tot
    pre_player2 = payer_details["Presenze"].iloc[0]
    amm_player2 = payer_details["Ammonizioni"].iloc[0]
    esp_player2 = payer_details["Espulsioni"].iloc[0]

    #print("__________")
    #print(pre_player2, amm_player2, esp_player2)

    # Prendiamo goal_fatti_tot, assist_tot, rigori_segnati_tot, rigori_parati_tot,
    #           goal_subiti_tot, autoreti_tot

    goal_fatti_tot = payer_details["Goal Fatti"].iloc[0]
    assist_tot = payer_details["Assist"].iloc[0]
    rigori_segnati_tot = payer_details["Rigori Segnati"].iloc[0]
    rigori_parati_tot = payer_details["Rigori Parati"].iloc[0]
    goal_subiti_tot = payer_details["Goal Subiti"].iloc[0]
    autoreti_tot = payer_details["Autogoal"].iloc[0]


    return html.H4([f'{pre_player2}']), html.H4([f'{amm_player2}']), html.H4([f'{esp_player2}']), html.H4([f'{goal_fatti_tot}']), html.H4([f'{assist_tot}']), html.H4([f'{rigori_segnati_tot}']), html.H4([f'{rigori_parati_tot}']), html.H4([f'{goal_subiti_tot}']), html.H4([f'{autoreti_tot}'])



# Gauge Callback Player 1
@app.callback(
    Output("gauge_p1", "figure"),
    Input("player1-dropdown", "value"),
    Input("season-dropdown", "value")
)

def gauge_p1(player1, season):
    value = [player1]
    stag = [season]
    # Filtriamo per il giocatore selezionato
    filtered_source = source[source["Giocatori"].isin(value)]
    filtered_source = filtered_source[filtered_source["stagione_partita"].isin(stag)]

    payer_details = filtered_source[0:1]

    #Prendiamo fantamedia e media voto PLAYER
    fmedia_player1 = payer_details["Fanta Media"].iloc[0]
    media_player1 = payer_details["Media Voto"].iloc[0]

    # Prendiamo fantamedia e media voto MAX
    max_fantamedia = source["Fanta Media"].max()
    max_mediavoto = source["Media Voto"].max()

    #print(fmedia_player1, media_player1)
    #print(max_fantamedia, max_mediavoto)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=fmedia_player1,
        domain={'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Media Voto", 'font': {'size': 24, "color": "#008080"}},
        gauge={
            'axis': {'range': [None, max_fantamedia], 'tickwidth': 2, 'tickcolor': "#662B8A"},
            'bar': {'color': "#662B8A"},
            'bgcolor': "#025464",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 3], 'color': '#D63222'},
                {'range': [3, 6], 'color': '#FFAD00'},
                {'range': [6, 9], 'color': '#44D62C'},
                {'range': [9, 10], 'color': '#0827F5'}],
            'threshold': {
                'line': {'color': "#008080", 'width': 3},
                'thickness': 0.95,
                'value': media_player1,
            }}))

    fig.update_layout(paper_bgcolor="black", font={'color': "#9400d3", 'family': "Arial"})
    fig.add_annotation(
        x=0.5,
        y=0.3,
        text="Fanta Media",
        showarrow=False,
        font=dict(
            size=20
        )
    )

    return fig


#____________________________________________________


# Gauge Callback Player 2
@app.callback(
    Output("gauge_p2", "figure"),
    Input("player2-dropdown", "value"),
    Input("season-dropdown", "value")
)

def gauge_p2(player2, season):
    value = [player2]
    stag = [season]
    # Filtriamo per il giocatore selezionato
    filtered_source = source[source["Giocatori"].isin(value)]
    filtered_source = filtered_source[filtered_source["stagione_partita"].isin(stag)]
    payer_details = filtered_source[0:1]

    #Prendiamo fantamedia e media voto PLAYER
    fmedia_player2 = payer_details["Fanta Media"].iloc[0]
    media_player2 = payer_details["Media Voto"].iloc[0]

    # Prendiamo fantamedia e media voto MAX
    max_fantamedia = source["Fanta Media"].max()
    max_mediavoto = source["Media Voto"].max()

    #print(fmedia_player2, media_player2)
    #print(max_fantamedia, max_mediavoto)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=fmedia_player2,
        domain={'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Media Voto", 'font': {'size': 24, "color": "#008080"}},
        gauge={
            'axis': {'range': [None, max_fantamedia], 'tickwidth': 2, 'tickcolor': "#662B8A"},
            'bar': {'color': "#662B8A"},
            'bgcolor': "#025464",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 3], 'color': '#D63222'},
                {'range': [3, 6], 'color': '#FFAD00'},
                {'range': [6, 9], 'color': '#44D62C'},
                {'range': [9, 10], 'color': '#0827F5'}],
            'threshold': {
                'line': {'color': "#008080", 'width': 3},
                'thickness': 0.95,
                'value': media_player2,
            }}))

    fig.update_layout(paper_bgcolor="black", font={'color': "#9400d3", 'family': "Arial"})
    fig.add_annotation(
        x=0.5,
        y=0.3,
        text="Fanta Media",
        showarrow=False,
        font=dict(
            size=20
        )
    )

    return fig




# Statistiche Giornate Callback

# PLAYER 1
@app.callback(
    Output("stats_giornate_p1", "figure"),
    Input("player1-dropdown", "value"),
    Input("season-dropdown", "value")
)

def stats_giornate_p1(player1, season):
    value = [player1]
    stag = [season]

    # Filtriamo per il giocatore selezionato
    filtered_source = source[source["Giocatori"].isin(value)]
    filtered_source = filtered_source[filtered_source["stagione_partita"].isin(stag)]


    # Ordiniamo per Giornata in modo crescente
    filtered_source["Giornata_Num"] = filtered_source["Giornata_Match"].str.extract('(\d+)').astype(int)
    filtered_source = filtered_source.sort_values(by='Giornata_Num')
    print(filtered_source.head())

    #Creiamo Scatter
    fig = px.scatter(filtered_source, x="Giornata_Match", y=["goal_fatti_partita", "goal_subiti_partita",
                                                             "rigori_parati_partita", "assist_partita",
                                                             "ammonizioni_partita","espulsioni_partita"],
                     color_discrete_sequence=["green", "greenyellow", "purple", "blue", "orange", "red"])

    fig.update_traces(marker=dict(size=20))
    fig.update_layout(

        plot_bgcolor="black",
        paper_bgcolor="black",

        xaxis=dict(showgrid=True, gridcolor="black",
                   title=dict(text="Giornata_Match", font=dict(color="white")),
                   tickfont=dict(size=12, color='#9400d3')),

        yaxis=dict(showgrid=True,
                   gridcolor="black",
                   tickfont=dict(size=12, color='#9400d3')),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="white")
        )
    )

    return fig


# PLAYER 2
@app.callback(
    Output("stats_giornate_p2", "figure"),
    Input("player2-dropdown", "value"),
    Input("season-dropdown", "value")
)

def stats_giornate_p2(player2, season):
    value = [player2]
    stag = [season]

    # Filtriamo per il giocatore selezionato
    filtered_source = source[source["Giocatori"].isin(value)]
    filtered_source = filtered_source[filtered_source["stagione_partita"].isin(stag)]


    # Ordiniamo per Giornata in modo crescente
    filtered_source["Giornata_Num"] = filtered_source["Giornata_Match"].str.extract('(\d+)').astype(int)
    filtered_source = filtered_source.sort_values(by='Giornata_Num')


    #Creiamo Scatter
    fig = px.scatter(filtered_source, x="Giornata_Match", y=["goal_fatti_partita", "goal_subiti_partita",
                                                             "rigori_parati_partita", "assist_partita",
                                                             "ammonizioni_partita","espulsioni_partita"],
                     color_discrete_sequence=["green", "greenyellow", "purple", "blue", "orange", "red"])

    fig.update_traces(marker=dict(size=20))
    fig.update_layout(

        plot_bgcolor="black",
        paper_bgcolor="black",

        xaxis=dict(showgrid=True, gridcolor="black",
                   title=dict(text="Giornata_Match", font=dict(color="white")),
                   tickfont=dict(size=12, color='#9400d3')),

        yaxis=dict(showgrid=True,
                   gridcolor="black",
                   tickfont=dict(size=12, color='#9400d3')),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="white")
        )
    )

    return fig



# Voti/Fantavoti Giornate Callback

# PLAYER 1
@app.callback(
    Output("voti_giornate_p1", "figure"),
    Input("player1-dropdown", "value"),
    Input("season-dropdown", "value")
)
def voti_giornate_p1(player1, season):
    value = [player1]
    stag = [season]

    #Filtriamo per il giocatore e anno selezionato
    filtered_source = source[source["Giocatori"].isin(value)]
    filtered_source = filtered_source[filtered_source["stagione_partita"].isin(stag)]


    # Ordiniamo per Giornata in modo crescente
    filtered_source["Giornata_Num"] = filtered_source["Giornata_Match"].str.extract('(\d+)').astype(int)
    filtered_source = filtered_source.sort_values(by='Giornata_Num')

    #Convertiamo in Float i valori numerici
    #print(filtered_source[['Fantavoto', "Voto"]])

    filtered_source['Fantavoto'] = filtered_source['Fantavoto'].astype(str).str.replace(',', '.')

    filtered_source['Voto'] = filtered_source['Voto'].replace('-', "0.0")
    filtered_source['Voto'] = filtered_source['Voto'].astype(float)
    filtered_source['Fantavoto'] = filtered_source['Fantavoto'].astype(float)


    #print(filtered_source[['Fantavoto', "Voto"]])

    # create a line chart with two traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_source['Giornata_Match'],
        y=filtered_source['Fantavoto'],
        name='Fantavoto',
        line_color='blue'
    ))
    fig.add_trace(go.Scatter(
        x=filtered_source['Giornata_Match'],
        y=filtered_source['Voto'],
        name='Voto',
        line_color='orange'
    ))

    # update layout
    fig.update_layout(
        title='Confronto tra Voto e Fantavoto',
        plot_bgcolor='black',
        paper_bgcolor='black',
        xaxis=dict(
            showgrid=True,
            gridcolor='black',
            title=dict(text='Giornata_Match', font=dict(color='darkviolet', size=16)),
            tickfont=dict(color='darkviolet', size=14)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='black',
            title=dict(text='Valore', font=dict(color='darkviolet', size=16)),
            tickfont=dict(color='darkviolet', size=14)
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(color='white')
        )
    )
    return fig




# PLAYER 2
@app.callback(
    Output("voti_giornate_p2", "figure"),
    Input("player2-dropdown", "value"),
    Input("season-dropdown", "value")
)
def voti_giornate_p1(player2, season):
    value = [player2]
    stag = [season]

    #Filtriamo per il giocatore e anno selezionato
    filtered_source = source[source["Giocatori"].isin(value)]
    filtered_source = filtered_source[filtered_source["stagione_partita"].isin(stag)]


    # Ordiniamo per Giornata in modo crescente
    filtered_source["Giornata_Num"] = filtered_source["Giornata_Match"].str.extract('(\d+)').astype(int)
    filtered_source = filtered_source.sort_values(by='Giornata_Num')

    #Convertiamo in Float i valori numerici
    #print(filtered_source[['Fantavoto', "Voto"]])

    filtered_source['Fantavoto'] = filtered_source['Fantavoto'].astype(str).str.replace(',', '.')

    filtered_source['Voto'] = filtered_source['Voto'].replace('-', "0.0")
    filtered_source['Voto'] = filtered_source['Voto'].astype(float)
    filtered_source['Fantavoto'] = filtered_source['Fantavoto'].astype(float)


    #print(filtered_source[['Fantavoto', "Voto"]])

    # create a line chart with two traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_source['Giornata_Match'],
        y=filtered_source['Fantavoto'],
        name='Fantavoto',
        line_color='blue'
    ))
    fig.add_trace(go.Scatter(
        x=filtered_source['Giornata_Match'],
        y=filtered_source['Voto'],
        name='Voto',
        line_color='orange'
    ))

    # update layout
    fig.update_layout(
        title='Confronto tra Voto e Fantavoto',
        plot_bgcolor='black',
        paper_bgcolor='black',
        xaxis=dict(
            showgrid=True,
            gridcolor='black',
            title=dict(text='Giornata_Match', font=dict(color='darkviolet', size=16)),
            tickfont=dict(color='darkviolet', size=14)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='black',
            title=dict(text='Valore', font=dict(color='darkviolet', size=16)),
            tickfont=dict(color='darkviolet', size=14)
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(color='white')
        )
    )
    return fig




if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8000)






