from dash import Dash
from layout import create_layout
from callback import callbacks

# Inicializar o aplicativo Dash
app = Dash(__name__)

#inicializar o servidor
server = app.server

# Configurar o layout
app.layout = create_layout()

#configurar callbacks
callbacks(app=app)

# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
