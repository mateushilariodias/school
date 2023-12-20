# school

mkdir myproject
cd myproject
py -3 -m venv .venv

.venv\Scripts\activate

pip install Flask

pip install mySQL.connector  

CREATE TABLE mateus_TB_student(
	nome VARCHAR(50),
	cpf VARCHAR(50) PRIMARY KEY,
	senha VARCHAR(50)
)

SELECT * FROM mateus_TB_student;

DROP TABLE mateus_TB_student;

CREATE TABLE mateus_TB_employee(
	nome VARCHAR(50),
	email VARCHAR(50),
	cpf VARCHAR(50),
	usuario VARCHAR(50) PRIMARY KEY,
	senha VARCHAR(50)
)

SELECT * FROM mateus_TB_employee;

DROP TABLE mateus_TB_employee;
 
INSERT INTO mateus_TB_employee(nome, email, cpf, usuario, senha) VALUE ('admin', 'admin@gmail.com', '445', 'admin', 123)

CREATE TABLE mateus_TB_discipline(
	disciplina VARCHAR(50) PRIMARY KEY
)

SELECT * FROM mateus_TB_discipline;

DROP TABLE mateus_TB_discipline;

CREATE TABLE mateus_TB_grade(
	cpf VARCHAR(50),
	disciplina VARCHAR(50),
	nome VARCHAR(50),
	nota1 VARCHAR(50),
	nota2 VARCHAR(50),
	nota3 VARCHAR(50),
	nota4 VARCHAR(50),
	PRIMARY KEY (cpf, disciplina)
)

SELECT * FROM mateus_TB_grade;

DROP TABLE mateus_TB_grade;