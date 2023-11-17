from flask import Flask, render_template, request, redirect, url_for;
import mysql.connector;

app = Flask(__name__);

@app.route('/')
def root():
    return render_template('homepage.html')

@app.route('/login-aluno')
def loginAlunoGet():
    return render_template('login-aluno.html')

# aqui captura os valores que vem por formulario e renderiza a página 
@app.route('/login-aluno', methods=['POST'])
def loginAlunoPost():
    alunoCpf = request.form['cpf']
    alunoSenha = request.form['senha']

    if alunoCpf == 'admin' and alunoSenha == '123':
        return redirect(url_for('homepage'))
    else:
        return redirect(url_for('inicio', titulo="Usuário ou senha inválido"))
    
@app.route('/login-aluno')
def loginAlunoGet():
    return render_template('login-aluno.html')

# aqui captura os valores que vem por formulario e renderiza a página 
@app.route('/login-aluno', methods=['POST'])
def loginAlunoPost():
    alunoCpf = request.form['cpf']
    alunoSenha = request.form['senha']

    if alunoCpf == 'admin' and alunoSenha == '123':
        return redirect(url_for('homepage'))
    else:
        return redirect(url_for('inicio', titulo="Usuário ou senha inválido"))
    


app.run(debug=True)