from flask import Flask, render_template, request, redirect, url_for;
import mysql.connector;

app = Flask(__name__);

@app.route('/')
def root():
    return render_template('homepage.html')

app.run(debug=True)