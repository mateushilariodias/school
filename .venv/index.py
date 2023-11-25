from flask import Flask, render_template, request, redirect, url_for, jsonify;
import mysql.connector;

app = Flask(__name__);

@app.route('/')
def root():
    return render_template('homepage.html')

def verificar_credenciais_aluno(cpf, senha):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = "SELECT * FROM mateus_TB_student WHERE cpf = %s AND senha = %s"
    cursor.execute(query, (cpf, senha))
    resultado = cursor.fetchone()

    conn.close()

    return resultado

# Função para obter informações do aluno
def get_student_info(cpf):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = 'SELECT cpf, nome FROM mateus_TB_student WHERE cpf = %s'
    cursor.execute(query, (cpf,))
    aluno_info = cursor.fetchone()

    conn.close()

    return aluno_info

# Função para obter notas do aluno
def get_student_grades(cpf):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = 'SELECT disciplina, nota1, nota2, nota3, nota4 FROM mateus_TB_grade WHERE cpf = %s'
    cursor.execute(query, (cpf,))
    grades = cursor.fetchall()

    conn.close()

    return grades

def calculate_average(grades):
    # Função para calcular a média das notas
    if not grades:
        return None

    averages = []

    for grade in grades:
        # Filtrar as notas que não são None
        valid_grades = [float(grade[i]) for i in range(1, 5) if grade[i] is not None]

        # Calcular a média
        if valid_grades:
            average = sum(valid_grades) / len(valid_grades)
            averages.append(round(average, 2))
        else:
            averages.append(None)

    return averages

# Rota para login do aluno
@app.route('/login-aluno', methods=['GET', 'POST'])
def loginAluno():
    if request.method == 'GET':
        return render_template('login-aluno.html')
    elif request.method == 'POST':
        aluno_cpf = request.form['cpf']
        aluno_senha = request.form['senha']

        # Verificar as credenciais do aluno
        resultado = verificar_credenciais_aluno(aluno_cpf, aluno_senha)

        if resultado:
            # Redirecionar para a página do aluno
            return redirect(url_for('homeStudentsGet', cpf=aluno_cpf))
        else:
            # Redirecionar para a página de login com uma mensagem de erro
            return redirect(url_for('loginAluno', error='CPF ou senha inválido'))

@app.route('/home-students/<cpf>')
def homeStudentsGet(cpf):
    # Obter informações do aluno
    aluno_info = get_student_info(cpf)

    if aluno_info:
        # Obter notas do aluno
        grades = get_student_grades(cpf)

        # Calcular a média das notas
        averages = calculate_average(grades)

        # Criar uma nova lista com a média para cada disciplina
        grades_with_average = [(grade[0], grade[1], grade[2], grade[3], grade[4], avg) for grade, avg in zip(grades, averages)]

        # Renderizar a página
        return render_template('home-students.html', aluno_info=aluno_info, grades=grades_with_average)
    else:
        # Tratar o caso em que o aluno não é encontrado
        return render_template('login-aluno.html')

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

@app.route('/login-aluno', methods=['POST'])
def loginAlunoPost():
    alunoCpf = request.form['cpf']
    alunoSenha = request.form['senha']

    resultado = verificar_credenciais_aluno(alunoCpf, alunoSenha)

    if resultado:
        return redirect(url_for('homeStudentsGet'))
    else:
        return redirect(url_for('loginAlunoGet', error='CPF ou senha inválido'))

def verificar_credenciais_aluno(cpf, senha):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = "SELECT * FROM mateus_TB_student WHERE cpf = %s AND senha = %s"
    cursor.execute(query, (cpf, senha))
    resultado = cursor.fetchone()

    conn.close()

    return resultado

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
    disciplina_anterior = request.form['disciplina_anterior']

    db = mysql.connector.connect(**db_config)
    mycursor = db.cursor()
    query = "UPDATE mateus_TB_discipline SET disciplina = '" + disciplina + "' WHERE disciplina = '" + disciplina_anterior + "'"

    mycursor.execute(query)
    db.commit()

    return redirect(url_for('cadastroDeDisciplina'))

def get_students():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = 'SELECT cpf, nome FROM mateus_TB_student'
    cursor.execute(query)
    students = cursor.fetchall()
    conn.close()
    return students

def get_disciplinas():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = 'SELECT disciplina FROM mateus_TB_discipline'
    cursor.execute(query)
    disciplinas = cursor.fetchall()
    conn.close()
    return disciplinas

def get_notas():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = '''
        SELECT G.cpf, G.disciplina, G.nome, G.nota1, G.nota2, G.nota3, G.nota4
        FROM mateus_TB_grade G
    '''
    cursor.execute(query)
    notas = cursor.fetchall()
    conn.close()
    return notas

@app.route('/get-cpf/<nome>')
def get_cpf_by_name(nome):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = 'SELECT cpf FROM mateus_TB_student WHERE nome = %s'
    cursor.execute(query, (nome,))
    cpf = cursor.fetchone()[0] if cursor.rowcount > 0 else None

    conn.close()
    return jsonify({'cpf': cpf})

@app.route('/cadastro-nota', methods=['GET', 'POST'])
def notasAluno():
    if request.method == 'GET':
        estudantes = get_students()
        disciplinas = get_disciplinas()
        notas = get_notas()
        return render_template('cadastro-nota.html', students=estudantes, disciplinas=disciplinas, notas=notas)
    elif request.method == 'POST':
        cpf = request.form['cpf']
        disciplina = request.form['disciplina']
        nome = request.form['nome']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Verificar se já existe uma entrada para o aluno e disciplina
        query_check_existence = 'SELECT * FROM mateus_TB_grade WHERE cpf = %s AND disciplina = %s'
        cursor.execute(query_check_existence, (cpf, disciplina))
        nota_existente = cursor.fetchone()

        if nota_existente:
            return redirect(url_for('notasAluno', error='Já cadastrado'))
        else:
            # Inserir nova nota se não existir uma entrada
            nota1 = request.form['nota1']
            nota2 = request.form['nota2']
            nota3 = request.form['nota3']
            nota4 = request.form['nota4']

            # Obtendo o nome do aluno
            query_nome_aluno = 'SELECT nome FROM mateus_TB_student WHERE cpf = %s'
            cursor.execute(query_nome_aluno, (cpf,))
            nome = cursor.fetchone()[0]

            query_insert = '''
                INSERT INTO mateus_TB_grade (cpf, disciplina, nome, nota1, nota2, nota3, nota4)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            values_insert = (cpf, disciplina, nome, nota1, nota2, nota3, nota4)
            cursor.execute(query_insert, values_insert)
            conn.commit()

        conn.close()
        return redirect(url_for('notasAluno'))

@app.route('/excluir-nota/<cpf>/<disciplina>')
def excluirNota(cpf, disciplina):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "DELETE FROM mateus_TB_grade WHERE cpf = %s AND disciplina = %s"
    cursor.execute(query, (cpf, disciplina))
    conn.commit()
    conn.close()
    return redirect(url_for('notasAluno'))

@app.route('/atualizar-nota/<cpf>/<disciplina>')
def atualizarNota(cpf, disciplina):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT cpf, disciplina, nome, nota1, nota2, nota3, nota4 FROM mateus_TB_grade WHERE cpf = %s AND disciplina = %s"
    cursor.execute(query, (cpf, disciplina))
    nota = cursor.fetchone()
    conn.close()
    return render_template('atualizacao-nota.html', notas=nota)

@app.route('/salvar-alteracao-nota', methods=['POST'])
def salvarAlteracaoNota():
    cpf = request.form['cpf']
    disciplina = request.form['disciplina']
    nome = request.form['nome']
    nota1 = float(request.form['nota1'])
    nota2 = float(request.form['nota2'])
    nota3 = float(request.form['nota3'])
    nota4 = float(request.form['nota4'])

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = '''
        UPDATE mateus_TB_grade
        SET nota1 = %s, nota2 = %s, nota3 = %s, nota4 = %s
        WHERE cpf = %s AND disciplina = %s
    '''
    values = (nota1, nota2, nota3, nota4, cpf, disciplina)
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return redirect(url_for('notasAluno'))

app.run(debug=True)