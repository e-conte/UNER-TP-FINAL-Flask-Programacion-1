from flask import Flask, render_template, request, url_for, redirect
import requests

import json

app = Flask(__name__, template_folder="templates",static_folder='../static')
app.config['FLASK_SKIP_CSRF'] = True
app.config["STATIC_FOLDER"] = "static"
app.config["STATIC_URL_PATH"] = "/static"


# Abrir y cargar el archivo clientes.json
with open('clientes.json', 'r') as clientes_file:
    clientes = json.load(clientes_file)

# Abrir y cargar el archivo ventas.json
with open('vehiculos.json', 'r') as vehiculos_file:
    vehiculos = json.load(vehiculos_file)
################################################################################
################################################################################
##############
##########      #      ######    #####  ####  ########
######        ####     #####    ####   ###########
###         ########    ##########    #######  #######


    





################################################################################
################################################################################
##############
##########      #      ######    #####  ####  ########
######        ####     #####    ####   ###########
###         ########    ##########    #######  #######


@app.route('/', methods=['GET', 'POST'])
def index():   
    lista_menu = [
        '1. Vehículos',
        '2. Clientes', 
        '3. Transacciones', 
        '4. Ver Cotización del Dolar',
        'Menú Principal',
        'Ir al Menú',
        'Concesionario La Ñata',
        'Bienvenido!'
    ]
  
    return render_template('index.html', lista_menu=lista_menu)


###############################################################
@app.route('/vehiculos', methods=['GET', 'POST'])
def vehiculos():
    lista_vehiculos = [
    '1. Crear Vehículos', 
    '2. Editar Vehículos', 
    '3. Eliminar Vehículo', 
    '4. Listar Vehículo', 
    '5. Buscar Vehículo',
    '6. Volver al Menú Principal',
    'Vehículos',
    'Ir al Menú',
    'Concesionario La Ñata',#h1
    'Bienvenido!'] #h2

    #opcion_menu_vehiculos = request.form.get('opcion')

    return render_template('vehiculos.html', **{'lista_vehiculos':lista_vehiculos})

@app.route('/vehiculos-crear', methods=['GET', 'POST'])
def vehiculos_crear():
    lista_crear = [
        'Concesionario La Ñata',  # h1
        'Bienvenido!',  # h2
        'Vehículo Nuevo',  # h3
        'Completa todos los campos', # h4
        'Volver a Vehículos', 
    ]
    return render_template('vehiculos-crear.html', lista_crear=lista_crear)

@app.route('/submit-c-v', methods=["POST"])
def vehiculos_crear_submit_form():

    with open('vehiculos.json', 'r') as file:
        vehiculos = json.load(file)
        
    form_data = request.form
    # Get the form data
    item_id = len(vehiculos) + 1

    nuevo_vehiculo = {
    'item_id':item_id,
    'patente': form_data.get('patente'),
    'marca': form_data.get('marca'),
    'modelo': form_data.get('modelo'),
    'tipo': form_data.get('tipo'),
    'anio': form_data.get('anio'),
    'kilometraje': form_data.get('kilometraje'),
    'precio_compra': form_data.get('precio_compra'),
    'precio_venta': form_data.get('precio_venta'),
    'estado': form_data.get('estado')
    }
    vehiculos.append(nuevo_vehiculo)
    with open('vehiculos.json', 'w') as file:
        json.dump(vehiculos, file, indent=4)
    print("Vehiculo creado correctamente.")
    return redirect(url_for("vehiculos"))


@app.route('/vehiculos-borrar', methods=['GET', 'POST'])
def vehiculos_borrar():
    lista_borrar = [
        'Concesionario La Ñata',  # h1
        'Bienvenido!',  # h2
        'Eliminar Vehículo',  # h3
        'Ingrese el ID o la Pantente del Vechículo que desea eliminar', #h4
        'Volver a Vehículos',
    ]
    return render_template('vehiculos-borrar.html', lista_borrar=lista_borrar)

@app.route("/submit-b-v", methods=["POST"])
def vehiculos_borrar_submit_form():
    patente = None
    with open('vehiculos.json', 'r') as file:
        vehiculos = json.load(file)
    #   cargamos los datos de json en memoria
    form_data = request.form
    #   traemos los datos del formulario
    try:
        item_id = int(form_data.get('item_id'))  # Convert item_id to integer
    except ValueError:
        item_id = 0
        patente = form_data.get('patente')

    if item_id != 0:
        parametro = 'item_id'
        data_a_buscar = item_id
    else:
        parametro = 'patente'
        data_a_buscar = patente
    
    for vehiculo in vehiculos:
        if vehiculo[parametro] == data_a_buscar:
            vehiculos.remove(vehiculo)
            break  # Exit the loop after removing the vehicle
    
    with open('vehiculos.json', 'w') as file:
        json.dump(vehiculos, file, indent=4)
    print("Vehiculo eliminado correctamente.")
    return redirect(url_for("vehiculos"))

@app.route('/vehiculos-pre-editar', methods=['POST','GET'])
def vehiculos_pre_editar():
    lista_pre_editar = [
        'Concesionario La Ñata',  # h1
        'Bienvenido!',  # h2
        'Editar Vehículo',  # h3
        'Ingrese el ID o la Patente del Vechículo que desea editar', # h4
        'Volver a Vehículos',
    ]    
    return render_template('vehiculos-pre-editar.html', lista_pre_editar=lista_pre_editar)

@app.route('/submit-pre-e-v', methods=['POST','GET'])
def vehiculos_pre_e_submit_form():
    global vehiculo_pre_editar
    
    form_data = request.form
    #   traemos los datos del formulario

    parametro = form_data.get('parametro') 

    vehiculo_pre_editar = parametro

    print(vehiculo_pre_editar)
    
    return redirect(url_for('vehiculos_editar'))

@app.route('/vehiculos_editar', methods=['GET', 'POST'])
def vehiculos_editar():
    lista_editar = [
        'Concesionario La Ñata',  # h1
        'Bienvenido!',  # h2
        'Editar Vehículo',  # h3
        'Ingrese los campos que desea editar', # h4
        'Volver a Vehículos',
    ]
    return render_template('vehiculos-editar.html', lista_editar=lista_editar)

@app.route('/submit-e-v', methods=['GET', 'POST'])
def vehiculos_editar_submit_form():
    with open('vehiculos.json', 'r') as file:
        vehiculos = json.load(file)
    #   cargamos los datos de json en memoria

    form_data = request.form
    #cargamos la data del form

    parametro = vehiculo_pre_editar # Obtenemos el parámetro del formulario

    if parametro.isdigit():
        parametro = int(parametro)
        editar_por = 'item_id'
        auxiliar_var=1
    else:
        parametro = vehiculo_pre_editar
        editar_por = 'patente'
        auxiliar_var=0
    diccionario_a_editar = None

    for registro in vehiculos:
        if registro.get(editar_por) == parametro:
            diccionario_a_editar=registro
            break
    
    if not diccionario_a_editar:
        print("No se encontró el vehículo")
        return redirect(url_for("vehiculos"))
    
    item_id = parametro

    patente =  form_data.get('patente') or diccionario_a_editar['patente']
    marca = form_data.get('marca') or diccionario_a_editar['marca']
    modelo = form_data.get('modelo') or diccionario_a_editar['modelo']
    tipo = form_data.get('tipo') or diccionario_a_editar['tipo']
    anio = form_data.get('anio') or diccionario_a_editar['anio']
    kilometraje = form_data.get('kilometraje') or diccionario_a_editar['kilometraje']
    precio_compra = form_data.get('precio_compra') or diccionario_a_editar['precio_compra']
    precio_venta = form_data.get('precio_venta') or diccionario_a_editar['precio_venta']
    estado = form_data.get('estado') or diccionario_a_editar['estado']

    vehiculo_form = {
        'item_id': item_id,
        'patente': patente,
        'marca': marca,
        'modelo': modelo,
        'tipo': tipo,
        'anio': anio,
        'kilometraje': kilometraje,
        'precio_compra': precio_compra,
        'precio_venta': precio_venta,
        'estado': estado,
        }

    print(vehiculo_form)

    for vehiculo in vehiculos:
        if vehiculo[editar_por] == parametro:
            vehiculo.update(vehiculo_form)
            break

    with open('vehiculos.json', 'w') as file:
        json.dump(vehiculos, file, indent=4)
    print("Vehiculo actualizado correctamente.")

    return redirect(url_for("vehiculos"))

@app.route("/vehiculos-listar", methods=["GET", "POST"])
def vehiculos_listar():
    
    with open('vehiculos.json', 'r') as file:
        vehiculos = json.load(file)
    #   cargamos los datos de json en memoria
    
    lista_listar = [
        'Concesionario La Ñata',  # h1
        'Bienvenido!',  # h2
        'Listar Vehículos',  # h3
        'Listado de Vehículos',  # h4
        'Volver a Vehículos',  # h5
    ]

    return render_template('vehiculos-listar.html', lista_listar=lista_listar, vehiculos= vehiculos)






################################################################################
################################################################################
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    lista_menu = [
    '1. Crear Cliente', 
    '2. Editar Cliente', 
    '3. Eliminar Cliente', 
    '4. Listar Clientes', 
    '5. Buscar Clientes', 
    '6. Volver al Menu Principal',
    'Menu Clientes',
    'Ir al Menú',
    'Concesionario La Ñata',#h1
    'Bienvenido!'] #h2


    opcion_menu_clientes = request.form.get('opcion')

    return render_template('clientes.html', **{'lista_menu': lista_menu})

@app.route('/transacciones', methods=['GET', 'POST'])
def transacciones():
    lista_menu = [
    '1. Crear Transacción', 
    '2. Listar Transacciones',
    '3. Buscar Transacción', 
    '4. Volver al Menú Principal',
    'Menu Transacciones',
    'Ir al Menú',
    'Concesionario La Ñata',#h1
    'Bienvenido!'] #h2


    opcion_menu_transacciones = request.form.get('opcion')

    return render_template('transacciones.html', **{'lista_menu': lista_menu})

#################### DOLAR OKEY ####################
@app.route('/cotizacion', methods=['GET', 'POST'])
def cotizacion_ppal():
    blue_string, oficial_string = obtener_cotizacion_dolar()

    lista_menu =  [
    'Cotizacion del Dolar',
    'Dolar Blue',
    'Dolar Oficial',
    'Volver al Menu Principal',
    'Concesionario La Ñata',#h1
    'Bienvenido!'] #h2 

    headers = ['Dolar Promedio','Dolar Venta','Dolar Compra']
    fields1 = [blue_string]  # Dólar Blue
    fields2 = [oficial_string]  # Dólar Oficial
        
    return render_template('cotizacion.html', **{'lista_menu': lista_menu, 'headers': headers, 'fields1':fields1, 'fields2':fields2})

        #Integrar la plantilla cotizacion.html proporcionada
def obtener_cotizacion_dolar():
    url = 'https://api.bluelytics.com.ar/v2/latest'
    response = requests.get(url)
    
    if response.status_code == 200:
        dolar = response.json()
        blue = dolar['blue']
        oficial = dolar['oficial']
        
        blue_string = [str(blue.get('value_avg')), str(blue.get('value_sell')), str(blue.get('value_buy'))]
        oficial_string = [str(oficial.get('value_avg')), str(oficial.get('value_sell')), str(oficial.get('value_buy'))]
        
        return blue_string, oficial_string
    else:
        return [], []
####################################################