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
        return redirect(url_for('homeStudentsGet'))
    else:
        return redirect(url_for('loginAlunoPost', error='CPF ou senha inválido'))

@app.route('/home-students')
def homeStudentsGet():
    return render_template('home-students.html')

@app.route('/login-secretaria')
def loginFuncionarioGet():
    return render_template('login-secretaria.html')

db_config = {
    'host':'mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com',
    'user':'aluno_fatec',
    'password':'aluno_fatec',
    'database':'meu_banco'
}

def verificar_credenciais(usuario, senha):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Executar uma consulta para verificar as credenciais
    query = "SELECT * FROM mateus_TB_employee WHERE usuario = %s AND senha = %s"
    cursor.execute(query, (usuario, senha))
    resultado = cursor.fetchone()

    conn.close()

    return resultado

@app.route('/login-secretaria', methods=['POST'])
def loginFuncionarioPost():
    funcionarioUsuario = request.form['usuario']
    funcionarioSenha = request.form['senha']

    resultado = verificar_credenciais(funcionarioUsuario, funcionarioSenha)

    if resultado:
        return redirect(url_for('homeSecretariaGet'))
    else:
        return redirect(url_for('loginFuncionarioPost', error="Usuário ou senha inválido"))
    
@app.route('/home-secretaria')
def homeSecretariaGet():
    return render_template('home-secretaria.html')

@app.route('/cadastro-aluno', methods=['POST'])
def cadastrarAluno():
    nome = request.form['nome']
    cpf = request.form['cpf']
    senha = request.form['senha']

    db = mysql.connector.connect(host='mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com',
                                 user='aluno_fatec',
                                 password='aluno_fatec',
                                 database='meu_banco')

    mycursor = db.cursor()

    query = 'INSERT INTO mateus_TB_student (nome, cpf, senha) VALUES (%s, %s, %s)'
    values = (nome, cpf, senha)

    mycursor.execute(query, values)

    db.commit()
    return redirect(url_for('cadastroDeAluno'))

@app.route('/cadastro-aluno')
def cadastroDeAluno():
    db = mysql.connector.connect(host='mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com',
                                 user='aluno_fatec',
                                 password='aluno_fatec',
                                 database='meu_banco')

    mycursor = db.cursor()
    query = 'SELECT cpf, nome FROM mateus_TB_student'
    mycursor.execute(query)
    students = mycursor.fetchall()
    return render_template('cadastro-aluno.html', cpfs=students)

@app.route('/excluir-aluno/<cpf>')
def excluirAluno(cpf):
    db = mysql.connector.connect(host='mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com',
                                 user='aluno_fatec',
                                 password='aluno_fatec',
                                 database='meu_banco')

    mycursor = db.cursor()
    query = "DELETE FROM mateus_TB_student WHERE cpf = '" + cpf + "'"
    mycursor.execute(query)
    db.commit()
    return redirect(url_for('cadastroDeAluno'))

@app.route('/atualizar-aluno/<cpf>')
def atualizarAluno(cpf):
    db = mysql.connector.connect(host='mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com',
                                 user='aluno_fatec',
                                 password='aluno_fatec',
                                 database='meu_banco')

    mycursor = db.cursor()
    query = "SELECT cpf, nome, senha FROM mateus_TB_student WHERE cpf = '" + cpf + "'"
    mycursor.execute(query)
    students = mycursor.fetchall()
    return render_template('atualizacao-aluno.html', cpfs=students)

@app.route('/salvar-alteracao-aluno', methods=['POST'])
def salvarAlteracaoAluno():
    cpf = request.form['cpf']
    nome = request.form['nome']
    senha = request.form['senha']

    db = mysql.connector.connect(host='mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com',
                                 user='aluno_fatec',
                                 password='aluno_fatec',
                                 database='meu_banco')

    mycursor = db.cursor()
    query = "UPDATE mateus_TB_student SET nome = %s, senha = %s WHERE cpf = %s"
    values = (nome, senha, cpf)
    mycursor.execute(query, values)
    db.commit()
    return redirect(url_for('cadastroDeAluno'))


def verificar_credenciais(usuario, senha):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Executar uma consulta para verificar as credenciais
    query = "SELECT * FROM mateus_TB_employee WHERE usuario = %s AND senha = %s"
    cursor.execute(query, (usuario, senha))
    resultado = cursor.fetchone()

    conn.close()

    return resultado

@app.route('/cadastro-funcionario', methods=['POST'])
def cadastrarFuncionario():
    nome = request.form['nome']
    email = request.form['email']
    cpf = request.form['cpf']
    usuario = request.form['usuario']
    senha = request.form['senha']

    db = mysql.connector.connect(**db_config)
    mycursor = db.cursor()

    query = 'INSERT INTO mateus_TB_employee (nome, email, cpf, usuario, senha) VALUES (%s, %s, %s, %s, %s)'
    values = (nome, email, cpf, usuario, senha)

    mycursor.execute(query, values)

    db.commit()
    return redirect(url_for('cadastroDeFuncionario'))

@app.route('/cadastro-funcionario')
def cadastroDeFuncionario():
    db = mysql.connector.connect(**db_config)
    mycursor = db.cursor()
    query = 'SELECT cpf, nome, email, usuario FROM mateus_TB_employee'
    mycursor.execute(query)
    employee = mycursor.fetchall()
    return render_template('cadastro-funcionario.html', usuarios=employee)

@app.route('/excluir-funcionario/<usuario>')
def excluirFuncionario(usuario):
    db = mysql.connector.connect(**db_config)
    mycursor = db.cursor()
    query = "DELETE FROM mateus_TB_employee WHERE usuario = '" + usuario + "'"
    mycursor.execute(query)
    db.commit()
    return redirect(url_for('cadastroDeFuncionario'))

@app.route('/atualizar-funcionario/<usuario>')
def atualizarFuncionario(usuario):
    db = mysql.connector.connect(**db_config)
    mycursor = db.cursor()
    query = "SELECT cpf, nome, email, usuario, senha FROM mateus_TB_employee WHERE usuario = %s"
    mycursor.execute(query, (usuario,))
    employee = mycursor.fetchall()
    return render_template('atualizacao-funcionario.html', usuarios=employee)

@app.route('/salvar-alteracao-funcionario', methods=['POST'])
def salvarAlteracaoFuncionario():
    usuario = request.form['usuario']
    cpf = request.form['cpf']
    nome = request.form['nome']
    email = request.form['email']

    db = mysql.connector.connect(**db_config)
    mycursor = db.cursor()
    query = "UPDATE mateus_TB_employee SET nome = %s, email = %s, cpf = %s WHERE usuario = %s"
    values = (nome, email, cpf, usuario)
    mycursor.execute(query, values)
    db.commit()
    return redirect(url_for('cadastroDeFuncionario'))

@app.route('/cadastro-disciplina', methods=['POST'])
def cadastrarDisciplina():
    disciplina = request.form['disciplina']

    db = mysql.connector.connect(**db_config)
    mycursor = db.cursor()

    query = 'INSERT INTO mateus_TB_discipline (disciplina) VALUES (%s)'
    values = (disciplina,)

    mycursor.execute(query, values)
    db.commit()

    return redirect(url_for('cadastroDeDisciplina'))

@app.route('/cadastro-disciplina')
def cadastroDeDisciplina():
    db = mysql.connector.connect(**db_config)
    mycursor = db.cursor()
    query = 'SELECT disciplina FROM mateus_TB_discipline'
    mycursor.execute(query)
    disciplinas = mycursor.fetchall()
    return render_template('cadastro-disciplina.html', disciplinas=disciplinas)

@app.route('/excluir-disciplina/<disciplina>')
def excluirDisciplina(disciplina):
    db = mysql.connector.connect(**db_config)
    mycursor = db.cursor()
    query = "DELETE FROM mateus_TB_discipline WHERE disciplina = %s"
    mycursor.execute(query, (disciplina,))
    db.commit()
    return redirect(url_for('cadastroDeDisciplina'))

@app.route('/atualizar-disciplina/<disciplina>')
def atualizarDisciplina(disciplina):
    db = mysql.connector.connect(**db_config)
    mycursor = db.cursor()
    query = "SELECT disciplina FROM mateus_TB_discipline WHERE disciplina = %s"
    mycursor.execute(query, (disciplina,))
    disciplinas = mycursor.fetchall()
    return render_template('atualizacao-disciplina.html', disciplinas=disciplinas)

@app.route('/salvar-alteracao-disciplina', methods=['POST'])
def salvarAlteracaoDisciplina():
    disciplina = request.form['disciplina']

    db = mysql.connector.connect(**db_config)
    mycursor = db.cursor()
    query = "INSERT INTO mateus_TB_discipline set disciplina = '" + disciplina + "' WHERE disciplina = "
    mycursor.execute(query)
    db.commit()

    return redirect(url_for('cadastroDeDisciplina'))

@app.route('/cadastro-nota')
def cadastroNotaGet():
    return render_template('cadastro-nota.html')

app.run(debug=True)