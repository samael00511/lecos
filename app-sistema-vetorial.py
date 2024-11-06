import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Inicializar o aplicativo Dash
app = Dash(__name__)

server = app.server

# Ler o arquivo Excel
file_path = 'Planilha Geral - Índice Trilema Brasil.xlsx'
df = pd.read_excel(file_path, sheet_name='Trilema energético')

# Derreter os dados filtrados para Equidade, Segurança e Ambiental
df_equidade = pd.melt(
    df,
    id_vars=['Região', 'Estado'],
    value_vars=['Equidade 2018', 'Equidade 2019', 'Equidade 2020', 'Equidade 2021', 'Equidade 2022'],
    var_name='Dimensão',
    value_name='Escala'
)

df_seguranca = pd.melt(
    df,
    id_vars=['Região', 'Estado'],
    value_vars=['Segurança 2018', 'Segurança 2019', 'Segurança 2020', 'Segurança 2021', 'Segurança 2022'],
    var_name='Dimensão',
    value_name='Escala'
)

df_ambiental = pd.melt(
    df,
    id_vars=['Região', 'Estado'],
    value_vars=['Ambiental 2018', 'Ambiental 2019', 'Ambiental 2020', 'Ambiental 2021', 'Ambiental 2022'],
    var_name='Dimensão',
    value_name='Escala'
)

df_ambiental['Ano'] = df_ambiental['Dimensão'].str.slice(-4)
df_equidade['Ano'] = df_equidade['Dimensão'].str.slice(-4)
df_seguranca['Ano'] = df_seguranca['Dimensão'].str.slice(-4)

# Obter todas as regiões únicas
estado = df_ambiental['Estado'].unique()
ano = df_ambiental['Ano'].unique()

# Layout do aplicativo
app.layout = html.Div(
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
                    "SISTEMA VETORIAL - TRILEMA ENERGÉTICO",  # Título
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
                        'width': '20%',
                        'height': '100%',
                        'display': 'flex', 
                        'minWidth': '250px',
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
                        html.Div(style={'height': '20px'}),  # Espaçamento entre as divs
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
                html.Div(style={'height': '400px', 'display': 'flex'}),  # Espaçamento entre as divs                
                html.Div(
                    style={
                        'width': '100%',  # Largura maior para acomodar os gráficos
                        'height': 'auto',
                        'flexDirection': 'columns',
                        'backgroundColor': '#457b9d',
                        'margin-left': '10px',
                        'margin-right': '10px',
                    },
                    children=[
                        html.Div(
                            style={
                                #'backgroundColor': '#EDF6F9',  
                                'width': '1520px',  # Largura maior para acomodar os gráficos
                                'height': '100px',
                                'margin-left': '30px',
                                'color': 'white'
                            },
                            children=[
                                html.H1(
                                "Este painel oferece uma comparação entre o sistema vetorial proposto na tése e entre o triângulo do trilema energético, proposto por parovic.",
                                style={
                                    'fontFamily' : 'Helvetica',
                                    'fontSize' : '16px',
                                }
                                )
                            ]
                        ),
                        # Div para os gráficos
                        html.Div(
                            style={
                                'display': 'flex',
                                'flexDirection': 'row',  # Alinhar os gráficos horizontalmente
                                'width': '100%',  # Largura maior para acomodar os gráficos
                                'height': '650px',
                                #'alignItems': 'center',
                                #'margin-left': '70px',
                                #'margin-right': '20px',
                                'margin-top': '0',
                                'alignItems': 'flex-start',
                                'alignItems': 'center',
                                'justifyContent': 'center',  # Espaçar os gráficos igualmente
                                'border-radius': '10px',
                                #'backgroundColor': '#bee1e6',
                            },
                            children=[
                                # Primeiro gráfico 3D
                                dcc.Graph(
                                    id='vetor-grafico',
                                    config={'displayModeBar': True},
                                    style={
                                        #'height': '100px', 
                                        #'width': '100px', 
                                        #'margin-left': '50px',
                                        #'margin-top': '50px',
                                        #'justifyContent': 'center',
                                        }  # Ajustando dimensões
                                ),
                                html.Div(style={'width': '20px'}),
                                dcc.Graph(
                                    id='ternario-grafico',
                                    config={'displayModeBar': True},
                                    style={
                                        #'height': '100px', 
                                        #'width': '100px', 
                                        #'margin-left': '20px',
                                        #'margin-top': '50px',
                                        #'backgroundColor': '#80ffdb'
                                        }  # Ajustando dimensões e espaçamento
                                )
                            ]
                        ),
                    ]
                    
                ),
            ]
        ),
    ]
)


# Callback para atualizar o gráfico com base na seleção do dropdown
@app.callback(
    [Output('vetor-grafico', 'figure'),
     Output('ternario-grafico', 'figure'),
     Output('angulo-ideal-x', 'children'),
     Output('angulo-ideal-y', 'children'),
     Output('angulo-ideal-z', 'children'),
     Output('angulo-generico-x', 'children'),
     Output('angulo-generico-y', 'children'),
     Output('angulo-generico-z', 'children'),
     Output('angulo-generico-ideal', 'children'),
     Output('angulo-ambiental-seguranca', 'children'),
     Output('angulo-ambiental-equidade', 'children'),
     Output('angulo-seguranca-equidade', 'children')],
    [Input('estado-dropdown', 'value'),
     Input('ano-dropdown', 'value')]
)
def atualizar_grafico(estado_selecionado, ano_selecionado):
    # Filtrar os dados pela região selecionada
    df_ambiental_filtrado = df_ambiental[(df_ambiental['Estado'] == estado_selecionado) &
                                         (df_ambiental['Ano'] == ano_selecionado)]
    
    df_seguranca_filtrado = df_seguranca[(df_seguranca['Estado'] == estado_selecionado) &
                                         (df_seguranca['Ano'] == ano_selecionado)]
    
    df_equidade_filtrado = df_equidade[(df_equidade['Estado'] == estado_selecionado) &
                                        (df_equidade['Ano'] == ano_selecionado)]

    # Somar os elementos
    equidade = df_equidade_filtrado['Escala'].sum()
    ambiental = df_ambiental_filtrado['Escala'].sum()
    seguranca = df_seguranca_filtrado['Escala'].sum()

    # Ponto de origem
    start = [0, 0, 0]

    # Vetor ideal
    ideal = [10, 10, 10]

    #vertices do tringulo
    
    vertices = [
        [equidade, 0, 0],
        [0, seguranca, 0],
        [0, 0, ambiental]
    ]

    vertices_ideal = [
        [ideal[0], 0, 0],
        [0, ideal[1], 0],
        [0, 0, ideal[2]]
    ]

    # Extraindo coordenadas x, y, z dos vértices
    x_vertices = [v[0] for v in vertices]
    y_vertices = [v[1] for v in vertices]
    z_vertices = [v[2] for v in vertices]

    # Extraindo coordenadas x, y, z dos vértices
    x_vertices_ideal = [v[0] for v in vertices_ideal]
    y_vertices_ideal = [v[1] for v in vertices_ideal]
    z_vertices_ideal = [v[2] for v in vertices_ideal]

    # Definindo a face do triângulo (conexão entre os vértices)
    faces = [[0, 1, 2]]  # Conexão entre A, B e C

    # Criar a figura
    fig1 = go.Figure()

    # Vetor genérico
    fig1.add_trace(go.Scatter3d(
        x=[start[0], equidade], y=[start[1], seguranca], z=[start[2], ambiental],
        mode='lines+markers',
        line=dict(color='red', width=5),
        marker=dict(size=4),
        name='Vetor genérico'
    ))

    # Vetor ideal
    fig1.add_trace(go.Scatter3d(
        x=[start[0], ideal[0]], y=[start[1], ideal[1]], z=[start[2], ideal[2]],
        mode='lines+markers',
        line=dict(color='blue', width=5),
        marker=dict(size=4),
        name='Vetor ideal'
    ))

    # projeções vetor ideal

    fig1.add_trace(go.Scatter3d(
        x=[start[0], ideal[0]], y=[start[1], 0], z=[start[2], 0],
        mode='lines+markers',
        line=dict(color='#1d3557', width=5),
        marker=dict(size=4),
        name='Vetor ideal x'
    ))

    fig1.add_trace(go.Scatter3d(
        x=[start[0], 0], y=[start[1], ideal[1]], z=[start[2], 0],
        mode='lines+markers',
        line=dict(color='#1d3557', width=5),
        marker=dict(size=4),
        name='Vetor ideal y'
    ))

    fig1.add_trace(go.Scatter3d(
        x=[start[0], 0], y=[start[1], 0], z=[start[2], ideal[2]],
        mode='lines+markers',
        line=dict(color='#1d3557', width=5),
        marker=dict(size=4),
        name='Vetor ideal z'
    ))

    # projeções vetor de analise

    fig1.add_trace(go.Scatter3d(
        x=[start[0], equidade], y=[start[1], 0], z=[start[2], 0],
        mode='lines+markers',
        line=dict(color='#ffba08', width=5),
        marker=dict(size=4),
        name='Vetor real x'
    ))

    fig1.add_trace(go.Scatter3d(
        x=[start[0], 0], y=[start[1], seguranca], z=[start[2], 0],
        mode='lines+markers',
        line=dict(color='#ffba08', width=5),
        marker=dict(size=4),
        name='Vetor real y'
    ))

    fig1.add_trace(go.Scatter3d(
        x=[start[0], 0], y=[start[1], 0], z=[start[2], ambiental],
        mode='lines+markers',
        line=dict(color='#ffba08', width=5),
        marker=dict(size=4),
        name='Vetor real z'
    ))

    # face triangular

    # Adicionando a superfície triangular
    fig1.add_trace(go.Mesh3d(
        x=x_vertices,
        y=y_vertices,
        z=z_vertices,
        i=[0],  # Índices das faces
        j=[1],
        k=[2],
        opacity=0.5,  # Opacidade da superfície
        color='red'  # Cor da superfície
    ))

    # Adicionando a superfície triangular
    fig1.add_trace(go.Mesh3d(
        x=x_vertices_ideal,
        y=y_vertices_ideal,
        z=z_vertices_ideal,
        i=[0],  # Índices das faces
        j=[1],
        k=[2],
        opacity=0.5,  # Opacidade da superfície
        color='lightblue'  # Cor da superfície
    ))

    # Ajustar limites dos eixos
    fig1.update_layout(
        scene=dict(
            xaxis=dict(range=[0, 10], title='Equidade Energética - x',showbackground=False,showgrid=False,zeroline=False),
            yaxis=dict(range=[0, 10], title='Segurança Energética - y',showbackground=False,showgrid=False,zeroline=False),
            zaxis=dict(range=[0, 10], title='Ambiental - z',showbackground=False,showgrid=False,zeroline=False),
            bgcolor="rgba(0,0,0,0)"
        ),
        title=f"Vetores 3D Interativos - Estado: {estado_selecionado}",
        height=600,
        width=750,
    )

    # Criar a figura para o gráfico ternário
    fig2 = go.Figure()

    # Adicionar o gráfico ternário
    fig2.add_trace(go.Scatterternary({
        'mode': 'markers',
        'a': [equidade],  # Equidade é o eixo A
        'b': [seguranca],  # Segurança é o eixo B
        'c': [ambiental],  # Ambiental é o eixo C
        'marker': {'symbol': 100, 'color': 'red', 'size': 14},
        'name': 'Dimensões Energéticas'
    }))

    #ponto de equilibrio
    equilibrio = [1/3, 1/3, 1/3]

    fig2.add_trace(go.Scatterternary({
        'mode': 'markers',
        'a': [equilibrio[0]],  # Equidade é o eixo A
        'b': [equilibrio[1]],  # Segurança é o eixo B
        'c': [equilibrio[2]],  # Ambiental é o eixo C
        'marker': {'symbol': 100, 'color': 'blue', 'size': 14},
        'name': 'Ponto de Equilibrio'
    }))

    # Configuração do gráfico ternário
    fig2.update_layout({
        'ternary': {
            'sum': 100,
            'aaxis': {'title': 'Equidade', 'min': 0, 'linewidth': 2, 'ticks': 'outside'},
            'baxis': {'title': 'Segurança', 'min': 0, 'linewidth': 2, 'ticks': 'outside'},
            'caxis': {'title': 'Ambiental', 'min': 0, 'linewidth': 2, 'ticks': 'outside'}
        },
        'title': f'Gráfico Ternário - Estado: {estado_selecionado}, Ano: {ano_selecionado}',
        'height': 600,
        'width': 750
    })



    # Calcular os ângulos de inclinação em relação aos eixos
    def calcular_angulo_eixo(vetor, eixo):
        return np.degrees(np.arccos(np.clip(np.dot(vetor, eixo) / (np.linalg.norm(vetor) * np.linalg.norm(eixo)), -1.0, 1.0)))

    def angulo_entre_eixos(cod1, cod2):
        return np.degrees(np.arctan(cod1 / cod2)) 

    # Vetores de referência dos eixos
    eixo_x = [1, 0, 0]
    eixo_y = [0, 1, 0]
    eixo_z = [0, 0, 1]

    angulo_yz = angulo_entre_eixos(ambiental, seguranca)
    angulo_xz = angulo_entre_eixos(ambiental, equidade)
    angulo_xy = angulo_entre_eixos(seguranca, equidade)

    # Calcular ângulos de inclinação
    angulo_ideal_x = calcular_angulo_eixo(ideal, eixo_x)
    angulo_ideal_y = calcular_angulo_eixo(ideal, eixo_y)
    angulo_ideal_z = calcular_angulo_eixo(ideal, eixo_z)

    angulo_generico_x = calcular_angulo_eixo([equidade, seguranca, ambiental], eixo_x)
    angulo_generico_y = calcular_angulo_eixo([equidade, seguranca, ambiental], eixo_y)
    angulo_generico_z = calcular_angulo_eixo([equidade, seguranca, ambiental], eixo_z)

    angulo_ideal_generico = calcular_angulo_eixo(ideal, [equidade, seguranca, ambiental])

    return (fig1,fig2,
            f"Eixo X: {angulo_ideal_x:.2f}°",
            f"Eixo Y: {angulo_ideal_y:.2f}°",
            f"Eixo Z: {angulo_ideal_z:.2f}°",
            f"Eixo X: {angulo_generico_x:.2f}°",
            f"Eixo Y: {angulo_generico_y:.2f}°",
            f"Eixo Z: {angulo_generico_z:.2f}°",
            f"Angulo entre vetor genérico e ideal: {angulo_ideal_generico:.2f}°",
            f"Ambiental e segurança: {angulo_yz:.2f}°",
            f"Ambiental e equidade: {angulo_xz:.2f}°",
            f"Segurança e equidade: {angulo_xy:.2f}°")

# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
