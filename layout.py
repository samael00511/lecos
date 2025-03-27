import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import data as dt

estado = dt.capturar_estado()
ano = dt.capturar_ano()

def create_layout():
    # Layout do aplicativo
    return html.Div(
        style={
            'height' : '100%',
            'width': '100%',  # Definindo a largura da Div
            'margin': '0 ',  # Centraliza a Div
            #'padding': '10px',  # Espaçamento interno
            'display': 'flex',  # Usar flexbox
            'flexDirection': 'column',  # Coloca o título primeiro e depois os elementos
            'alignItems': 'center',  # Centraliza os itens
            'backgroundColor': '#EDF6F9',
            'display': 'flex',
        },
        children=[
            # Adicionando o título no topo
            html.Div(
                style={
                    'height' : '50px',
                    'width': '100%',
                    'backgroundColor': '#0677BB',
                    'marginBottom': '10px',
                },
                children=[
                    html.H1(
                        "Sistema Vetorial Tridimensional da Transição Energética Justa em Nível Subnacional",  # Título
                        style={
                            'textAlign': 'left',  # Centralizar o texto
                            'fontFamily': 'Helvetica',
                            'fontSize': '30px',  # Tamanho da fonte
                            'margin-top' : '0',
                            'margin-left' : '10px',
                            'color': '#EDF6F9',
                            'backgroundColor': '#0677BB',
                            'height' : '50px',
                            'display': 'flex',
                            'alignItems': 'center', 

                        }
                    ),
                ]
            ),
            # Conteúdo principal em linha
            html.Div(
                style={
                    'display': 'flex',  # Usar flexbox para layout em linha
                    'flexDirection': 'row',  # Colocar os elementos em linha (horizontal)
                    'width': '100%',  # Usar toda a largura
                    'flexWarp': 'warp',
                    #'justifyContent': 'center',  # centraliza em tamanhos maiores
                },
                children=[
                    # Div esquerda (dropdowns e informações)
                    html.Div(
                        style={
                            'width': '30%',
                            'height': '100%',
                            'display': 'flex', 
                            #'minWidth': '250px',
                            'flexDirection': 'column',  # Coloca dropdowns em coluna
                            'margin-left': '10px' ,# Espaçamento à direita
                            'backgroundColor': '#0677BB',
                            #'margin-top': '30px',
                            'justifyContent': 'center',
                            'color': 'white'
                            
                        },
                        children=[
                            html.H1("Filtros", style={'fontFamily' : 'Helvetica', 'fontSize': '18px', 'margin-left' : '10px'}),
                            dcc.Dropdown(
                                id='estado-dropdown',
                                options=[{'label': estado, 'value': estado} for estado in estado],
                                value=estado[0],  # Valor padrão
                                clearable=False,
                                style={
                                    'width': '90%',
                                    'fontFamily' : 'Helvetica',
                                    'fontSize' : '16px',
                                    'color' : 'black',
                                    'margin-left' : '5px',
                                }
                            ),
                            dcc.Dropdown(
                                id='ano-dropdown',
                                options=[{'label': ano, 'value': ano} for ano in ano],
                                value=ano[0],  # Valor padrão
                                clearable=False,
                                style={
                                    'fontFamily' : 'Helvetica',
                                    'fontSize' : '16px',
                                    'color' : 'black',
                                    'margin-left' : '5px',
                                    'width': '90%',
                                }
                            ),
                            html.Div(style={'height': '2%'}),  # Espaçamento entre as divs
                            html.Div(
                                id='angulos-div',
                                style={
                                    'width' : '270px',
                                    'padding' : '10px',
                                    #'border' : '1px solid #ddd',
                                    #'border-radius': '10px',
                                    #'margin-left' : '0px',
                                    'color': 'white',
                                    #'display': 'None'
                                    #'alignItems': 'left',
                                    #'alignItems': 'flex-start',
                                    'justifyContent': 'left'
                                },
                                children=[
                                    html.H3("Ângulos de Inclinação", style={'fontFamily' : 'Helvetica',}),
                                    html.Hr(),
                                    html.P("Comparação entre cada um dos eixos com o vetor ideal ", style={'fontFamily' : 'Helvetica', 'fontSize' : '16px'}),
                                    html.P(id='angulo-ideal-x', style={'padding-left' : '20px','fontFamily' : 'Helvetica'}),
                                    html.P(id='angulo-ideal-y', style={'padding-left' : '20px','fontFamily' : 'Helvetica'}),
                                    html.P(id='angulo-ideal-z', style={'padding-left' : '20px','fontFamily' : 'Helvetica'}),
                                    html.Hr(),
                                    html.P("Comparação entre cada um dos eixos com o vetor genérico", style={'fontFamily' : 'Helvetica', 'fontSize' : '16px'}),
                                    html.P(id='angulo-generico-x', style={'padding-left' : '20px','fontFamily' : 'Helvetica'}),
                                    html.P(id='angulo-generico-y', style={'padding-left' : '20px','fontFamily' : 'Helvetica'}),
                                    html.P(id='angulo-generico-z', style={'padding-left' : '20px','fontFamily' : 'Helvetica'}),
                                    html.Hr(),
                                    html.P(id='angulo-generico-ideal', style={'fontFamily' : 'Helvetica'}),
                                    html.Hr(),
                                    html.P("Comparação das dimensões entre si", style={'fontFamily' : 'Helvetica'}),
                                    html.P(id='angulo-ambiental-seguranca', style={'padding-left' : '20px','fontFamily' : 'Helvetica'}),
                                    html.P(id='angulo-ambiental-equidade', style={'padding-left' : '20px','fontFamily' : 'Helvetica'}),
                                    html.P(id='angulo-seguranca-equidade', style={'padding-left' : '20px','fontFamily' : 'Helvetica'}),
                                ]
                            )
                        ],
                    ),
                    # html.Div(style={'height': '400px', 'display': 'flex'}),  # Espaçamento entre as divs                
                    html.Div(
                        style={
                            'width': '100%',  # Largura maior para acomodar os gráficos
                            'height': '1000px', # 900px
                            'flexDirection': 'column', # row
                            'backgroundColor': '#457b9d',
                            'margin-left': '10px',
                            'margin-right': '10px',
                        },
                        children=[
                            html.Div(
                                style={
                                    'margin': '10px',
                                    'display': 'flex',
                                    #'justifyContent': 'right',
                                    'fontSize' : '12px'
                                },
                                children=[
                                    html.Button("Mostrar Gráfico", id='show-graph-btn', n_clicks=0, style={'fontSize' : '25px'}),
                                    html.Button("Mostrar GIF", id='show-gif-btn', n_clicks=0, style={'fontSize' : '25px'}),
                                ]
                            ),
                            html.Div(
                                style={
                                    'flexDirection': 'column',
                                },
                                children=[
                                    html.Div(
                                        style={
                                            'fontFamily' : 'Helvetica',
                                            'color' : 'white',
                                            'margin-left': '20px',
                                            'fontsize': '16px',
                                        },
                                        children=[
                                            html.P("Abaixo temos uma figura que permiti visualizar de forma interativa a tendência de crescimento dos vetores."),
                                            ]
                                    ),
                                    # Div para os gráficos
                                    html.Div(
                                        style={
                                            'marginTop': '20px',
                                            'textAlign': 'center',
                                            'display': 'flex',
                                            'flexDirection': 'column',  # Organiza os elementos de conteúdo em coluna
                                            'alignItems': 'center',  # Centraliza os elementos
                                                        },
                                        children=[
                                            # Primeiro gráfico 3D
                                            dcc.Graph(
                                                id='vetor-grafico',
                                                config={'displayModeBar': True},
                                            ),
                                            html.Img(
                                                        id='gif-image',
                                                        src='',
                                                        style={'width': '720px', 'height': '820px','display': 'none'}
                                                    ),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                        
                    ),
                ]
            ),
        ]
    )