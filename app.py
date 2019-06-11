from flask import Flask, render_template, request

app = Flask(__name__)


def gravar(v1, v2):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS usr (usr txt, pwd txt)")
    db.execute("INSERT INTO usr VALUES (?,?)", (v1, v2))
    ficheiro.commit()
    ficheiro.close()
    return


def alterar(v1, v2):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS usr (usr txt, pwd txt)")
    db.execute("UPDATE usr SET pwd = ? WHERE usr = ?", (v1, v2))
    ficheiro.commit()
    ficheiro.close()
    return


def existe(v1, ):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE usr = ? and pwd= ?", (v1,))
    valor = db.fetchone()
    ficheiro.commit()
    ficheiro.close()
    return valor


def log(v1, v2):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE usr = ? and pwd = ?", (v1, v2,))
    valor = db.fetchone()
    ficheiro.close()
    return valor


def eliminar(v1):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("DELETE FROM usr WHERE usr = ? ", (v1,))
    ficheiro.commit()
    ficheiro.close()
    return


@app.route('/newpass', methods=['GET', 'POST'])
def newpass():
    erro = None
    if request.method == 'POST':
        v1 = request.form['usr']
        v2 = request.form['pwd']
        v3 = request.form['cpwd']
        if not existe(v1):
            erro = 'O utilizador não existe.'
        elif v2 != v3:
            erro = 'A palavra passe não coincide.'
        else:
            alterar(v1, v2)
    return render_template('newpass.html', erro=erro)


@app.route('/registo', methods=['GET', 'POST'])
def registo():
    erro = None
    if request.method == 'POST':
        v1 = request.form['usr']
        v2 = request.form['pwd']
        v3 = request.form['cpwd']
        if existe(v1):
            erro = 'O utilizador já existe.'
        elif v2 != v3:
            erro = 'A palavra passe não coincide.'
        else:
            gravar(v1, v2)
            erro = 'Utilizador  registado com sucesso'
    return render_template('registo.html', erro=erro)


@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        v1 = request.form['usr']
        v2 = request.form['pwd']
        if not existe(v1):
            erro = 'O utilizador já existe.'
        elif not log(v1, v2):
            erro = 'A palavra passe não coincide.'
        else:
            erro = 'Bem-vindo'
    return render_template('login.html', erro=erro)


@app.route('/apagar', methods=['GET', 'POST'])
def apagar():
    erro = None
    if request.method == 'POST':
        v1 = request.form['usr']
        v2 = request.form['pwd']
        if not existe(v1):
            erro = 'O utilizador não existe.'
        elif not log(v1, v2):
            erro = 'A palavra passe incorreta.'
        else:
            eliminar(v1)
            erro = 'Conta eliminada com sucesso'
    return render_template('apagar.html', erro=erro)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
