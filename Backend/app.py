from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Olá, Flask! Minha primeira rota.'

#ponto de entrada para rodar o servidor
if __name__ == '__main__':
    app.run(debug=True)