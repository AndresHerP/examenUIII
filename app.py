from flask import Flask, jsonify, render_template_string, request, abort,redirect, url_for
app = Flask(__name__)

dispositivos = {}

def calcular_otro(ip, nombre):
    ultimo_octeto = int(ip.split('.')[-1])
    longitud_nombre = len(nombre)
    nombre_formateado = nombre.replace(" ", "_")
    return f"{ultimo_octeto * 3 + longitud_nombre}:{nombre_formateado}"

@app.route('/dispositivos_html', methods=['GET'])
def dispositivos_html():
    html = """
    <html>
    <head>
        <style>
            .dispositivo {
                border: 1px solid #ccc;
                padding: 10px;
                margin: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Lista de Dispositivos</h1>
        {% for id, disp in dispositivos.items() %}
        <div class="dispositivo">
            <strong>Nombre:</strong> {{ disp['nombre'] }}<br>
            <strong>Descripción:</strong> {{ disp['descripcion'] }}<br>
            <strong>IP:</strong> {{ disp['ip'] }}<br>
            <strong>MAC:</strong> {{ disp['mac'] }}<br>
            <strong>Ubicación:</strong> {{ disp['ubicacion'] }}<br>
            <strong>Tipo:</strong> {{ disp['tipo'] }}<br>
            <strong>Otros:</strong> {{ disp['otros'] }}<br>
        </div>
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html, dispositivos=dispositivos)

@app.route('/dispositivos', methods=['POST'])
def agregar_dispositivo():
    data = request.json
    id_disp = data.get('id')
    if not id_disp:
        return jsonify({"error": "Se requiere un ID"}), 400

    if id_disp in dispositivos:
        return jsonify({"error": "El dispositivo ya existe"}), 400

    nombre = data.get('nombre', '')
    ip = data.get('ip', '')
    otros = calcular_otro(ip, nombre)

    dispositivos[id_disp] = {
        "nombre": nombre,
        "descripcion": data.get('descripcion', ''),
        "ip": ip,
        "mac": data.get('mac', ''),
        "ubicacion": data.get('ubicacion', ''),
        "tipo": data.get('tipo', ''),
        "otros": otros
    }

    return jsonify({"mensaje": "Dispositivo agregado", "dispositivo": dispositivos[id_disp]}), 201

@app.route('/dispositivos/<id_disp>', methods=['PUT'])
def modificar_dispositivo(id_disp):
    if id_disp not in dispositivos:
        return jsonify({"error": "Dispositivo no encontrado"}), 404

    data = request.json
    nombre = data.get('nombre', dispositivos[id_disp]['nombre'])
    ip = data.get('ip', dispositivos[id_disp]['ip'])
    otros = calcular_otro(ip, nombre)

    dispositivos[id_disp].update({
        "nombre": nombre,
        "descripcion": data.get('descripcion', dispositivos[id_disp]['descripcion']),
        "ip": ip,
        "mac": data.get('mac', dispositivos[id_disp]['mac']),
        "ubicacion": data.get('ubicacion', dispositivos[id_disp]['ubicacion']),
        "tipo": data.get('tipo', dispositivos[id_disp]['tipo']),
        "otros": otros
    })

    return jsonify({"mensaje": "Dispositivo modificado", "dispositivo": dispositivos[id_disp]})
    
@app.route('/', methods=['GET'])
def test():
    return "Hola mundo"

if __name__ == '__main__':
    app.run(debug=True)
