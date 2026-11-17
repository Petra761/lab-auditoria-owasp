import os
import psycopg2
from flask import Flask, request, jsonify, make_response
from markupsafe import escape

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "devuser"),
        password=os.getenv("DB_PASSWORD", "devpassword123"),
        dbname=os.getenv("DB_NAME", "banco_dev")
    )

# -------------------------------------------------------------
# Remediación 1: Consulta SQL Parametrizada y escape XSS Reflejado
# -------------------------------------------------------------
@app.route('/api/socios/buscar', methods=['GET'])
def buscar_socio():
    termino = request.args.get('q', '')
    conn = get_connection()
    cur = conn.cursor()
    
    # Uso de consulta parametrizada nativa con ILIKE para evitar SQLi
    query = "SELECT id, username, nombre_completo, saldo FROM usuarios WHERE nombre_completo ILIKE %s;"
    try:
        cur.execute(query, (f"%{termino}%",))
        filas = cur.fetchall()
        cur.close()
        conn.close()
        resultados = [{"id": f[0], "username": f[1], "nombre": f[2], "saldo": float(f[3])} for f in filas]
        
        # Sanitización de la entrada reflejada para prevenir XSS
        termino_seguro = escape(termino)
        mensaje = f"<p>Resultados obtenidos para el criterio: {termino_seguro}</p>"
        return make_response(jsonify({"filtro": mensaje, "data": resultados}), 200)
    except Exception as e:
        # Se evita la fuga de información técnica detallada del motor
        return jsonify({"error": "Ocurrió un error interno en el servidor."}), 500

# -------------------------------------------------------------
# Remediación 2: Control Anti-BOLA / IDOR
# -------------------------------------------------------------
@app.route('/api/socios/<int:usuario_id>/perfil', methods=['GET'])
def ver_perfil(usuario_id):
    # Validación de identidad mediante cabeceras de control simuladas
    solicitante_id = request.headers.get('X-User-Id')
    solicitante_rol = request.headers.get('X-User-Rol', 'cliente')
    
    # Si no es admin y el ID solicitado no coincide con el autenticado, se deniega el acceso
    if solicitante_rol != 'admin' and str(solicitante_id) != str(usuario_id):
        return jsonify({"error": "Acceso denegado: No autorizado para ver este perfil (BOLA prevenido)."}), 403

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, nombre_completo, ci, saldo, rol FROM usuarios WHERE id = %s;", (usuario_id,))
    u = cur.fetchone()
    cur.close()
    conn.close()
    
    if not u:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
        
    return jsonify({
        "id": u[0],
        "username": u[1],
        "nombre": u[2],
        "ci": u[3],
        "saldo": float(u[4]),
        "rol": u[5]
    }), 200

# -------------------------------------------------------------
# Remediación 3: Sanitización de XSS Almacenado
# -------------------------------------------------------------
@app.route('/api/comentarios', methods=['GET', 'POST'])
def comentarios():
    conn = get_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        data = request.get_json() or {}
        autor = escape(data.get('autor', 'Anonimo'))
        # Sanitización estricta del mensaje para evitar Stored XSS
        mensaje = escape(data.get('mensaje', ''))
        
        cur.execute("INSERT INTO comentarios (autor, mensaje) VALUES (%s, %s);", (autor, mensaje))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "comentario registrado"}), 201
    else:
        cur.execute("SELECT autor, mensaje FROM comentarios ORDER BY id DESC;")
        items = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{"autor": i[0], "mensaje": i[1]} for i in items]), 200

# -------------------------------------------------------------
# Remediación 4: Cabeceras de Seguridad y Supresión de Versiones
# -------------------------------------------------------------
@app.after_request
def aplicar_cabeceras(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = "default-src 'self'; frame-ancestors 'none';"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Eliminar cabeceras reveladoras de tecnología
    response.headers.pop('Server', None)
    response.headers.pop('X-Powered-By', None)
    return response

if __name__ == '__main__':
    # Desactivación del modo debug para evitar consola interactiva remota
    app.run(host='0.0.0.0', port=5000, debug=False)