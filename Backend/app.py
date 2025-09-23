from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bloqueado = db.Column(db.Boolean, nullable=False, default=False)
    def __repr__(self):
        return f"Usuario(id={self.id}, nome='{self.nome}', email='{self.email}')"

@app.route('/usuarios')
def gerenciar_usuarios():
    novo_usuario = Usuario(nome='Joao Silva', email='joao@exemplo.com')
    db.session.add(novo_usuario)
    db.session.commit()
    usuarios = Usuario.query.all()
    lista_de_usuarios = [f'{u.id} - {u.nome} - {u.email} - Bloqueado: {u.bloqueado}' for u in usuarios]
    return "<h1>Usuários:</h1>" + "<br>".join(lista_de_usuarios)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)