from urllib.parse import urlparse
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import User, db, Venta, get_user
import forms
import os
from datetime import datetime
from sqlalchemy import extract
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_login import current_user, login_user

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)
app.secret_key = "pipsas"

app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
login_manager = LoginManager(app)

#===============# ARCHIVO DE GUARDADO TEMP #===============#
ARCHIVO_TEMPORAL = 'pipsas.txt'

#===============# LEER EN TEMP #===============#
def leer_pizzas_temporales():
    pizzas = []
    if os.path.exists(ARCHIVO_TEMPORAL):
        with open(ARCHIVO_TEMPORAL, 'r') as archivo:
            for linea in archivo.readlines():
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split('|')
                if len(partes) == 6:
                    tamano, jamon_str, pina_str, champi_str, num_str, sub_str = partes
                    jamon = (jamon_str == 'True')
                    pina = (pina_str == 'True')
                    champi = (champi_str == 'True')
                    numero = int(num_str)
                    subtotal = float(sub_str)
                    lista_ingredientes = []
                    if jamon: lista_ingredientes.append('Jamón')
                    if pina: lista_ingredientes.append('Piña')
                    if champi: lista_ingredientes.append('Champiñones')
                    pizza = {
                        'tamano': tamano,
                        'ingredientes': ', '.join(lista_ingredientes),
                        'jamon': jamon,
                        'pina': pina,
                        'champi': champi,
                        'numero': numero,
                        'subtotal': subtotal
                    }
                    pizzas.append(pizza)
    return pizzas

#===============# ESCRIBIR EN TEMP #===============#
def escribir_pizzas_temporales(pizzas):
    with open(ARCHIVO_TEMPORAL, 'w') as archivo:
        for pizza in pizzas:
            linea = f"{pizza['tamano']}|{pizza['jamon']}|{pizza['pina']}|{pizza['champi']}|{pizza['numero']}|{pizza['subtotal']}\n"
            archivo.write(linea)
            
#===============# SUBTOTAL #===============#
def calcular_subtotal(tamano, jamon, pina, champi, numero):
    precios_tamano = {'Chica': 40, 'Mediana': 80, 'Grande': 120}
    precio_base = precios_tamano.get(tamano, 50)
    precio_ingredientes = (10 if jamon else 0) + (10 if pina else 0) + (10 if champi else 0)
    return (precio_base + precio_ingredientes) * numero

#===============# RUTA PRINCIPAL #===============#
@app.route('/puntoVenta', methods=['GET', 'POST'])
@login_required
def index():
    formulario_pizza = forms.PizzaForm(request.form)
    formulario_ventas = forms.ConsultaVentasForm(request.form)
    
    pizzas = leer_pizzas_temporales()
    subtotal_general = sum([pizza['subtotal'] for pizza in pizzas])
    
    ventas_resultado = []
    total_dia_mes = 0
    ventas_agrupadas = {}

    if request.method == 'POST':
        if 'tamano' in request.form:
            formulario_pizza.tamano.data = request.form['tamano']

        #===============# FORMULARIO RUTA DE PIZZA #===============#
        if formulario_pizza.btn_agregar.data or formulario_pizza.btn_quitar.data or formulario_pizza.btn_terminar.data:
            if formulario_pizza.btn_agregar.data:
                if not formulario_pizza.validate():
                    flash("Por favor, corrige los errores en el formulario.", "error")
                    return render_template('puntoVenta.html', pizza_form=formulario_pizza, ventas_form=formulario_ventas,
                                           pizzas=pizzas, subtotal_general=subtotal_general,
                                           ventas=ventas_resultado, agrupado=ventas_agrupadas, total_dia_mes=total_dia_mes)

                session['nombre'] = formulario_pizza.nombre.data
                session['direccion'] = formulario_pizza.direccion.data
                session['telefono'] = formulario_pizza.telefono.data
                session['fecha'] = formulario_pizza.fecha.data.strftime('%Y-%m-%d') if formulario_pizza.fecha.data else ''

                tamano = formulario_pizza.tamano.data
                jamon = formulario_pizza.jamon.data
                pina = formulario_pizza.pina.data
                champi = formulario_pizza.champi.data
                numero = formulario_pizza.numero_pizzas.data

                subtotal = calcular_subtotal(tamano, jamon, pina, champi, numero)
                nuevo_item = {
                    'tamano': tamano,
                    'jamon': jamon,
                    'pina': pina,
                    'champi': champi,
                    'numero': numero,
                    'subtotal': subtotal
                }
                lista_ingredientes = []
                if jamon: lista_ingredientes.append('Jamón')
                if pina: lista_ingredientes.append('Piña')
                if champi: lista_ingredientes.append('Champiñones')
                nuevo_item['ingredientes'] = ', '.join(lista_ingredientes)

                pizzas.append(nuevo_item)
                escribir_pizzas_temporales(pizzas)
                flash('Pizza agregada al pedido.', 'success')
                return redirect(url_for('index'))
            
            #===============# MODIFICACIONES EN TXT #===============#
            elif formulario_pizza.btn_quitar.data:
                if pizzas:
                    pizzas.pop()
                    escribir_pizzas_temporales(pizzas)
                    flash('Última pizza eliminada del pedido.', 'info')
                else:
                    flash('No hay pizzas para eliminar.', 'warning')
                return redirect(url_for('index'))

            elif formulario_pizza.btn_terminar.data:
                if pizzas:
                    total = sum([pizza['subtotal'] for pizza in pizzas])
                    nombre = formulario_pizza.nombre.data or session.get('nombre', '')
                    direccion = formulario_pizza.direccion.data or session.get('direccion', '')
                    telefono = formulario_pizza.telefono.data or session.get('telefono', '')
                    if formulario_pizza.fecha.data:
                        fecha = formulario_pizza.fecha.data
                    else:
                        try:
                            fecha = datetime.strptime(session.get('fecha', ''), '%Y-%m-%d').date()
                        except Exception:
                            fecha = None

                    nueva_venta = Venta(
                        nombre=nombre,
                        direccion=direccion,
                        telefono=telefono,
                        fecha_pedido=fecha,
                        total=total
                    )
                    db.session.add(nueva_venta)
                    db.session.commit()
                    flash(f"Pedido terminado. Total a pagar: ${total}", 'success')
                    escribir_pizzas_temporales([])
                    session.pop('nombre', None)
                    session.pop('direccion', None)
                    session.pop('telefono', None)
                    session.pop('fecha', None)
                else:
                    flash("No hay pizzas en el pedido.", 'error')
                return redirect(url_for('index'))
        
        elif formulario_ventas.btn_buscar.data and formulario_ventas.validate():
            tipo = formulario_ventas.tipo_busqueda.data
            fecha = formulario_ventas.fecha_busqueda.data  
            if tipo == 'dia':
                ventas_resultado = Venta.query.filter(Venta.fecha_pedido == fecha).all()
            else:
                ventas_resultado = Venta.query.filter(
                    extract('month', Venta.fecha_pedido) == fecha.month,
                    extract('year', Venta.fecha_pedido) == fecha.year
                ).all()
            total_dia_mes = sum(v.total for v in ventas_resultado)
            for venta in ventas_resultado:
                ventas_agrupadas[venta.nombre] = ventas_agrupadas.get(venta.nombre, 0) + venta.total

    if request.method == 'GET':
        if 'nombre' in session:
            formulario_pizza.nombre.data = session.get('nombre')
        if 'direccion' in session:
            formulario_pizza.direccion.data = session.get('direccion')
        if 'telefono' in session:
            formulario_pizza.telefono.data = session.get('telefono')
        if 'fecha' in session:
            try:
                formulario_pizza.fecha.data = datetime.strptime(session.get('fecha'), '%Y-%m-%d')
            except:
                pass

    return render_template('puntoVenta.html', pizza_form=formulario_pizza, ventas_form=formulario_ventas,
                           pizzas=pizzas, subtotal_general=subtotal_general,
                           ventas=ventas_resultado, agrupado=ventas_agrupadas, total_dia_mes=total_dia_mes)

#===============# RUTA PARA ELIMINAR UNA PIZZA ESPECÍFICA #===============#
@app.route('/eliminar_pizza/<int:index>', methods=['POST'])
def eliminar_pizza(index):
    pizzas = leer_pizzas_temporales()
    if 0 <= index < len(pizzas):
        pizzas.pop(index)
        escribir_pizzas_temporales(pizzas)
        flash("Pizza eliminada del pedido.", "success")
    else:
        flash("Pizza no encontrada.", "error")
    return redirect(url_for('index'))

#===============# RUTA LOGIN #===============#
@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = get_user(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)

#===============# RUTA SIGNUP #===============#
@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = forms.SignupForm()
    if form.validate_on_submit():
        username = form.username.data  # Usamos el campo "username"
        email = form.email.data
        password = form.password.data
        # Creamos el usuario y lo guardamos
        user = User(name=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        next_page = request.args.get('next', None)
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("signup_form.html", form=form)


#===============# RUTA LOGOUT #===============#
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_user(email):
    return User.query.filter_by(email=email).first()

#===============# 
if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3000)
