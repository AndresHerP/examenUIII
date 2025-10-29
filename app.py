from flask import Flask, jsonify, render_template_string, request, abort,redirect, url_for
app = Flask(__name__)

dispositivos = {}

def calcular_otro(ip, nombre):
    ultimo_octeto = int(ip.split('.')[-1])
    longitud_nombre = len(nombre)
    nombre_formateado = nombre.replace(" ", "_")
    return f"{ultimo_octeto * 3 + longitud_nombre}:{nombre_formateado}"


@app.route('/', methods=['GET'])
def home():
    return render_template_string("""
    <h1>Welcome to the Home Page</h1>
    <p>This is a simple Flask application.</p>
    <a href="{{ url_for('about') }}">About</a>
    """)