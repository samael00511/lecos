import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output
import data as dt
import os

df_ambiental = dt.tratamento_ambiental()
df_seguranca = dt.tratamento_seguranca()
df_equidade = dt.tratamento_equidade()

# Diretório onde estão os GIFs
GIF_FOLDER = "assets/"


'''
def callbacks(app):
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

'''
def callbacks(app):
# Callback para alternar visibilidade
    @app.callback(
        [Output('vetor-grafico', 'style'), 
         Output('gif-image', 'style'),
         Output('gif-image', 'src')],
        [Input('show-graph-btn', 'n_clicks'), 
         Input('show-gif-btn', 'n_clicks'),
         Input('estado-dropdown', 'value')]
    )

    def toggle_visibility(show_graph_clicks, show_gif_clicks,estado_selecionado):
        gif_filename = f"{estado_selecionado}.gif"  # Exemplo: CEARA.gif
        gif_path = os.path.join(GIF_FOLDER, gif_filename)

        if not os.path.isfile(gif_path):
            gif_path = ""  # Caminho vazio caso o GIF não exista

        
        # Se "Mostrar Gráfico" for clicado
        if show_graph_clicks > show_gif_clicks:
            return {'marginTop': '20px', 'height': '600px'}, {'display': 'none'},""
        # Se "Mostrar GIF" for clicado
        elif show_gif_clicks > show_graph_clicks:
            return {'display': 'none'}, {'width': '820px', 'height': '720px'},gif_path
        # Caso inicial
        return {'marginTop': '20px', 'height': '600px'}, {'display': 'none'},""


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