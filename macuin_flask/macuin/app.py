from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'macuin-secret-key-2026'

# ── Datos de ejemplo ──────────────────────────────────────────
PRODUCTOS = [
    {"id": 1, "nombre": "Aceite de Motor Multigrado Mobil Super", "precio": 350, "categoria": "Productos", "imagen": "aceite.png"},
    {"id": 2, "nombre": "Alternador Duralast Gold 13S5BN", "precio": 2789, "categoria": "Refacciones", "imagen": "alternador.png"},
    {"id": 3, "nombre": "Bujia de Platino NGK G-Power 96002", "precio": 259, "categoria": "Refacciones", "imagen": "bujia.png"},
    {"id": 4, "nombre": "Filtro de Aire STP ST11674", "precio": 419, "categoria": "Refacciones", "imagen": "filtro.png"},
    {"id": 5, "nombre": "Amortiguador (Strut) Duralast 433-7427-1R", "precio": 899, "categoria": "Refacciones", "imagen": "amortiguador.png"},
    {"id": 6, "nombre": "Rotor de Frenos de Disco Duralast Gold F-DL54111", "precio": 1549, "categoria": "Refacciones", "imagen": "rotor.png"},
    {"id": 7, "nombre": "Bateria de Plomo Acido Duralast Gold 34-DLG", "precio": 3339, "categoria": "Productos", "imagen": "bateria.png"},
    {"id": 8, "nombre": "Philips Standard Luz Delantera H4666C1", "precio": 670, "categoria": "Exteriores", "imagen": "faro.png"},
]

PEDIDOS = [
    {"id": "002556", "fecha": "16 de Abr, 2026", "total": 1699, "estatus": "Pendiente",
     "items": [{"nombre": "Bujia de Platino NGK", "precio": 259, "cantidad": 1, "subtotal": 259},
               {"nombre": "Filtro de Aire STP", "precio": 419, "cantidad": 1, "subtotal": 419}]},
    {"id": "001545", "fecha": "01 de Feb, 2026", "total": 2999, "estatus": "Completado",
     "items": [{"nombre": "Aceite de Motor Mobil Super", "precio": 350, "cantidad": 2, "subtotal": 700}]},
    {"id": "001897", "fecha": "22 de Mar, 2026", "total": 399,  "estatus": "Enviado",
     "items": [{"nombre": "Bujia de Platino NGK", "precio": 259, "cantidad": 1, "subtotal": 259}]},
    {"id": "001569", "fecha": "28 de Jun, 2026", "total": 5787, "estatus": "Completado",
     "items": [
         {"nombre": "Amortiguador (Strut) Duralast 433-7427-1R", "precio": 899, "cantidad": 1, "subtotal": 899, "imagen": "amortiguador.png"},
         {"nombre": "Rotor de Frenos de Disco Duralast Gold F-DL54111", "precio": 1549, "cantidad": 1, "subtotal": 1549, "imagen": "rotor.png"},
         {"nombre": "Bateria de Plomo Acido Duralast Gold 34-DLG", "precio": 3339, "cantidad": 1, "subtotal": 3339, "imagen": "bateria.png"},
     ]},
]

# ── Rutas ──────────────────────────────────────────────────────
@app.route('/')
def index():
    return redirect(url_for('catalogo'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Aquí va la validación real con BD
        if email and password:
            session['usuario'] = email
            return redirect(url_for('catalogo'))
        flash('Credenciales incorrectas', 'error')
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmar = request.form.get('confirmar')
        if password != confirmar:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('registro.html')
        # Aquí va el registro real
        session['usuario'] = email
        return redirect(url_for('catalogo'))
    return render_template('registro.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/catalogo')
def catalogo():
    categoria = request.args.get('categoria', '')
    busqueda = request.args.get('q', '')
    precio_min = int(request.args.get('precio_min', 200))
    precio_max = int(request.args.get('precio_max', 10000))
    marcas = request.args.getlist('marca')

    productos = PRODUCTOS
    if categoria:
        productos = [p for p in productos if p['categoria'] == categoria]
    if busqueda:
        productos = [p for p in productos if busqueda.lower() in p['nombre'].lower()]
    productos = [p for p in productos if precio_min <= p['precio'] <= precio_max]

    return render_template('catalogo.html', productos=productos, categoria=categoria, busqueda=busqueda)

@app.route('/carrito')
def carrito():
    carrito_items = session.get('carrito', [])
    subtotal = sum(item['precio'] * item['cantidad'] for item in carrito_items)
    return render_template('carrito.html', carrito=carrito_items, subtotal=subtotal)

@app.route('/carrito/agregar/<int:producto_id>', methods=['POST'])
def agregar_carrito(producto_id):
    producto = next((p for p in PRODUCTOS if p['id'] == producto_id), None)
    if producto:
        carrito = session.get('carrito', [])
        existente = next((i for i in carrito if i['id'] == producto_id), None)
        if existente:
            existente['cantidad'] += 1
        else:
            carrito.append({"id": producto['id'], "nombre": producto['nombre'],
                            "precio": producto['precio'], "cantidad": 1, "imagen": producto['imagen']})
        session['carrito'] = carrito
        session.modified = True
    return redirect(url_for('catalogo'))

@app.route('/carrito/actualizar/<int:producto_id>', methods=['POST'])
def actualizar_carrito(producto_id):
    accion = request.form.get('accion')
    carrito = session.get('carrito', [])
    for item in carrito:
        if item['id'] == producto_id:
            if accion == 'aumentar':
                item['cantidad'] += 1
            elif accion == 'disminuir' and item['cantidad'] > 1:
                item['cantidad'] -= 1
            elif accion == 'eliminar':
                carrito.remove(item)
            break
    session['carrito'] = carrito
    session.modified = True
    return redirect(url_for('carrito'))

@app.route('/historial')
def historial():
    filtro = request.args.get('filtro', 'Todos')
    busqueda = request.args.get('q', '')
    pedidos = PEDIDOS
    if filtro != 'Todos':
        pedidos = [p for p in pedidos if p['estatus'] == filtro]
    if busqueda:
        pedidos = [p for p in pedidos if busqueda in p['id']]
    return render_template('historial.html', pedidos=pedidos, filtro=filtro)

@app.route('/pedido/<pedido_id>')
def detalle_pedido(pedido_id):
    pedido = next((p for p in PEDIDOS if p['id'] == pedido_id), None)
    if not pedido:
        return redirect(url_for('historial'))
    return render_template('detalle_pedido.html', pedido=pedido)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
