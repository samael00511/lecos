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
                        'height': '900px',
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
                                'flexDirection': 'row',
                            },
                            children=[
                                html.Div(
                                    style={
                                        'fontFamily' : 'Helvetica',
                                        'color' : 'white',
                                    },
                                    children=[
                                        html.P("2018: O Sistema Vetorial Tridimensional da Transição Energética do Ceará para o ano de 2018 revela um desequilíbrio entre as dimensões que compõem o sistema. Esta representação ilustra os desafios enfrentados pelo estado no contexto da transição energética e aponta para a necessidade de medidas integradas e direcionadas para mitigar o desequilíbrio entre as dimensões. Para o ano de 2018, a dimensão de Equidade Energética é a que apresenta uma maior lacuna quando comparada a figura vetorial ideal, aumentando assim, a urgência de políticas públicas que promovam a redução das desigualdades no acesso à energia, especialmente para populações vulneráveis. Nesta dimensão indicadores que impactaram negativamente foram: subsídios à energia renovável, IDH e Índice de GINI. Além disso, as dimensões de Segurança Energética e Gestão Ambiental exigem fortalecimento por meio de estratégias que garantam a estabilidade do fornecimento de energia, promovam o uso sustentável dos recursos naturais e minimizem os impactos ambientais. O equilíbrio entre essas dimensões é essencial para que o Ceará avance de forma consistente em direção a uma transição energética justa e sustentável."),
                                        html.P("2019: O Sistema Vetorial Tridimensional da Transição Energética do Ceará para o ano de 2019, assim como em 2018, revela ainda um desequilíbrio entre as dimensões que compõem o sistema. Mais uma vez a dimensão de Equidade Energética é a que apresenta uma maior lacuna quando comparada a figura vetorial ideal, aumentando assim, a urgência de políticas públicas que promovam a redução das desigualdades no acesso à energia, especialmente para populações vulneráveis. Além disso, a dimensão de Gestão Ambiental apresentou um resultado inferior ao ano anterior. Este resultado foi impactado por indicadores como consumo de água per capita, acesso a água, esgoto não tratado e mortes por problemas respiratórios."),
                                        html.P("2020: O Sistema Vetorial Tridimensional da Transição Energética do Ceará para o ano de 2020, assim como em 2018 e 2019, revela uma redução discreta no desequilíbrio entre as dimensões que compõem o sistema. Mais uma vez a dimensão de Equidade Energética é a que apresenta a maior lacuna quando comparada a figura vetorial ideal. Este resultado foi impactado por indicadores como subsídios à energia renovável, IDH e Índice de GINI. "),
                                        html.P("2021: O Sistema Vetorial Tridimensional da Transição Energética do Ceará em 2021, revela mais uma vez a dimensão de Equidade Energética é a que apresenta a maior lacuna quando comparada a figura vetorial ideal. Este resultado foi impactado por indicadores como subsídios à energia renovável, IDH e Índice de GINI."),
                                        html.P("2022: O Sistema Vetorial Tridimensional da Transição Energética do Ceará para o ano de 2022, revela uma redução no desequilíbrio entre as dimensões que compõem o sistema. Mais uma vez a dimensão de Equidade Energética é a que apresenta a maior lacuna quando comparada a figura vetorial ideal. Este resultado foi impactado mais uma vez, por indicadores como subsídios à energia renovável, IDH e Índice de GINI.")
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
                                                    src='/assets/CEARÁ.gif',
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

# Callback para alternar visibilidade
@app.callback(
    [Output('vetor-grafico', 'style'), Output('gif-image', 'style')],
    [Input('show-graph-btn', 'n_clicks'), Input('show-gif-btn', 'n_clicks')]
)
def toggle_visibility(show_graph_clicks, show_gif_clicks):
    # Se "Mostrar Gráfico" for clicado
    if show_graph_clicks > show_gif_clicks:
        return {'marginTop': '20px', 'height': '600px'}, {'display': 'none'}
    # Se "Mostrar GIF" for clicado
    elif show_gif_clicks > show_graph_clicks:
        return {'display': 'none'}, {'width': '820px', 'height': '720px'}
    # Caso inicial
    return {'marginTop': '20px', 'height': '600px'}, {'display': 'none'}


# Callback para atualizar o gráfico com base na seleção do dropdown
@app.callback(
    [Output('vetor-grafico', 'figure'),
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
        name='Generic vector'
    ))

    # Vetor ideal
    fig1.add_trace(go.Scatter3d(
        x=[start[0], ideal[0]], y=[start[1], ideal[1]], z=[start[2], ideal[2]],
        mode='lines+markers',
        line=dict(color='blue', width=5),
        marker=dict(size=4),
        name='Ideal vector'
    ))

    # projeções vetor ideal

    fig1.add_trace(go.Scatter3d(
        x=[start[0], ideal[0]], y=[start[1], 0], z=[start[2], 0],
        mode='lines+markers',
        line=dict(color='#1d3557', width=5),
        marker=dict(size=4),
        name='Ideal vector x'
    ))

    fig1.add_trace(go.Scatter3d(
        x=[start[0], 0], y=[start[1], ideal[1]], z=[start[2], 0],
        mode='lines+markers',
        line=dict(color='#1d3557', width=5),
        marker=dict(size=4),
        name='Ideal vector y'
    ))

    fig1.add_trace(go.Scatter3d(
        x=[start[0], 0], y=[start[1], 0], z=[start[2], ideal[2]],
        mode='lines+markers',
        line=dict(color='#1d3557', width=5),
        marker=dict(size=4),
        name='Ideal vector z'
    ))

    # projeções vetor de analise

    fig1.add_trace(go.Scatter3d(
        x=[start[0], equidade], y=[start[1], 0], z=[start[2], 0],
        mode='lines+markers',
        line=dict(color='#ffba08', width=5),
        marker=dict(size=4),
        name='Royal vector x'
    ))

    fig1.add_trace(go.Scatter3d(
        x=[start[0], 0], y=[start[1], seguranca], z=[start[2], 0],
        mode='lines+markers',
        line=dict(color='#ffba08', width=5),
        marker=dict(size=4),
        name='Royal vector y'
    ))

    fig1.add_trace(go.Scatter3d(
        x=[start[0], 0], y=[start[1], 0], z=[start[2], ambiental],
        mode='lines+markers',
        line=dict(color='#ffba08', width=5),
        marker=dict(size=4),
        name='Royal vector z'
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
            xaxis=dict(range=[0, 10], title='Equity - x',showbackground=False,showgrid=False,zeroline=False),
            yaxis=dict(range=[0, 10], title='Security - y',showbackground=False,showgrid=False,zeroline=False),
            zaxis=dict(range=[0, 10], title='Environmental - z',showbackground=False,showgrid=False,zeroline=False),
            bgcolor="rgba(0,0,0,0)"
        ),
        title=f"Interactive 3D Vectors : {estado_selecionado} - {ano_selecionado}",
        height=720,
        width=820,
    )

   

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

    return (fig1,
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
