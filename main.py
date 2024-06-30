from flask import Flask, render_template, request, url_for, redirect, flash
from datetime import datetime
import requests
import json


app = Flask(__name__, template_folder="templates",static_folder='../static')
app.config['FLASK_SKIP_CSRF'] = True
app.config["STATIC_FOLDER"] = "static"
app.config["STATIC_URL_PATH"] = "/static"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# Abrir y cargar el archivo clientes.json
with open('clientes.json', 'r') as clientes_file:
    clientes = json.load(clientes_file)

# Abrir y cargar el archivo ventas.json
with open('vehiculos.json', 'r') as vehiculos_file:
    vehiculos = json.load(vehiculos_file)

# Abrir y cargar el archivo transacciones.json
#with open('transaciones.json', 'r') as transaciones_file:
 #       transacciones = json.load(transacciones_file)

################################################################################
# Comenzo flujo del programa
################################################################################

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

@app.route('/submit-c-v', methods=["POST", "GET"])
def vehiculos_crear_submit_form():

    with open('vehiculos.json', 'r') as file:
        vehiculos = json.load(file)
        
    form_data = request.form

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
    flash("Vehiculo creado correctamente")
    return redirect(url_for("vehiculos_crear"))


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
      
    button_label = request.form.get('submit')

    messsage="?"

    for vehiculo in vehiculos:
        if vehiculo[parametro] == data_a_buscar:
            vehiculos.remove(vehiculo)
            messsage ='borrado'

            break  # Exit the loop after removing the vehicle


    if messsage == 'borrado':
        print("Cliente eliminado correctamente.")
        flash("Cliente eliminado correctamente.")
    else:
        print("No se encontró el cliente")
        flash("No se encontró el cliente")

    
    with open('vehiculos.json', 'w') as file:
        json.dump(vehiculos, file, indent=4)
        

    return redirect(url_for("vehiculos_borrar"))

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
    
    if parametro.isdigit(): #
        parametro = int(parametro)
        editar_por = 'item_id'
        
    else:
        parametro = vehiculo_pre_editar
        editar_por = 'patente'
        diccionario_a_editar = None

    for registro in vehiculos:
        if registro.get(editar_por) == parametro:
            diccionario_a_editar=registro
            break

    if not diccionario_a_editar:
        print("No se encontró el vehículo")
        flash("No se encontró el cliente")
        return redirect(url_for("vehiculos_editar"))
    
    item_id = parametro

    if editar_por == 'patente':
        item_id = diccionario_a_editar['item_id']
    

    patente =  form_data.get('patente') or diccionario_a_editar['patente']
    marca = form_data.get('marca') or diccionario_a_editar['marca']
    modelo = form_data.get('modelo') or diccionario_a_editar['modelo']
    tipo = form_data.get('tipo') or diccionario_a_editar['tipo']
    anio = form_data.get('anio') or diccionario_a_editar['anio']
    kilometraje = form_data.get('kilometraje') or diccionario_a_editar['kilometraje']
    precio_compra = form_data.get('precio_compra') or diccionario_a_editar['precio_compra']
    precio_venta = form_data.get('precio_venta') or diccionario_a_editar['precio_venta']
    estado = form_data.get('estado') or diccionario_a_editar['estado']

    cliente_form = {
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

    print(cliente_form)

    for vehiculo in vehiculos:
        if vehiculo[editar_por] == parametro:
            vehiculo.update(cliente_form)
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
        'Listado de Vehículos',  # h3
        'Volver a Vehículos',
    ]

    return render_template('vehiculos-listar.html', lista_listar=lista_listar, vehiculos= vehiculos)
####################################################################
@app.route('/vehiculos-pre-buscar/', methods=["GET", "POST"])
def vehiculo_pre_buscar():
    lista_pre_buscar = [
        'Concesionario La Ñata',  # h1
        'Bienvenido!',  # h2
        'Buscar Vehículo',  # h3
        'Ingrese el ID o la Patente del Vehículo que desea buscar', # h4
        'Volver a Vehículos',
    ]
    return render_template('vehiculos-pre-buscar.html', lista_pre_buscar=lista_pre_buscar)

@app.route("/vehiculos-pre-b-v", methods=["GET", "POST"])
def vehiculos_pre_b_submit_form():
    with open('vehiculos.json', 'r') as file:
        vehiculos = json.load(file)
        #   cargamos los datos de json en memoria

    global dic_busqueda

    form_data = request.form
    parametro_vehiculo = form_data.get('parametro_vehiculo')
    campo_vehiculo = form_data.get('campo_vehiculo')

    for vehiculo in vehiculos:
        if vehiculo.get('campo_vehiculo') == parametro_vehiculo:
            dic_busqueda = vehiculo
            print(dic_busqueda)

    return redirect(url_for("vehiculos_buscar"))

@app.route("/vehiculos-buscar", methods=["GET", "POST"])
def vehiculos_buscar():
   
    dic_busqueda= vehiculos
    #   cargamos los datos de json en memoria
    
    lista_buscar = [
        'Concesionario La Ñata',  # h1
        'Bienvenido!',  # h2
        'Listado de Vehículos',  # h3
        'Volver a Vehículos',
    ]

    return render_template('vehiculos-buscar.html', lista_buscar=lista_buscar, vehiculos=vehiculos)




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

@app.route("/clientes-listar", methods=["GET", "POST"])
def clientes_listar():
    
    with open('clientes.json', 'r') as file:
        clientes = json.load(file)
    #   cargamos los datos de json en memoria
    
    lista_listar = [
        'Concesionario La Ñata',  # h1
        'Bienvenido!',  # h2
        'Listado de Clientes',  # h3
        'Volver a Clientes',
    ]

    return render_template('clientes-listar.html', lista_listar=lista_listar, clientes = clientes)
@app.route('/clientes-crear', methods=['GET', 'POST'])
def clientes_crear():
    lista_crear = [
        'Concesionario La Ñata',  # h1
        'Bienvenido!',  # h2
        'Crear Cliente',  # h3
        'Ingrese los datos del Cliente',  # h4
        'Volver a Clientes',
    ]
    return render_template('clientes-crear.html', lista_crear=lista_crear)

@app.route('/submit-c-c', methods=['POST'])
def clientes_crear_submit_form():

    with open('clientes.json', 'r') as file:
        clientes = json.load(file)

    form_data = request.form

    item_id = len(clientes) + 1

    nuevo_cliente = {
    'item_id': item_id,
    'nombre': form_data.get('nombre'),
    'apellido': form_data.get('apellido'),
    'documento': form_data.get('documento'),
    'direccion': form_data.get('direccion'),
    'telefono': form_data.get('telefono'),
    'correo_electronico': form_data.get('correo_electronico'),
    }

    clientes.append(nuevo_cliente)
    with open('clientes.json', 'w') as file:
        json.dump(clientes, file, indent=4)
    print("Cliente creado correctamente.")
    flash('Cliente creado correctamente.')

    return redirect(url_for('clientes'))
################################################################
@app.route('/clientes-borrar', methods=['GET','POST'])
def clientes_borrar():
    lista_borrar = [
        'Concesionario La Ñata',  # h1
        'Bienvenido!',  # h2
        'Eliminar Cliente',  # h3
        'Ingrese el ID del Cliente o Documento que desea eliminar',  # h4
        'Volver a Clientes',
    ]
    return render_template('clientes-borrar.html', lista_borrar=lista_borrar)

@app.route('/submit-b-c', methods=['POST'])
def clientes_borrar_submit_form():
    documento = None
    with open('clientes.json', 'r') as file:
        clientes = json.load(file)

        form_data = request.form
    
    try:
        item_id = int(form_data.get('item_id'))
    except ValueError:
        item_id = 0
        documento = form_data.get('documento')

    if item_id !=0:
        parametro = 'item_id'
        data_a_buscar = item_id
    else:
        parametro = 'documento'
        data_a_buscar = documento

    button_label = request.form.get('submit')

    messsage="?"

    for cliente in clientes:
        if cliente[parametro] == data_a_buscar:
            clientes.remove(cliente)
            messsage ='borrado'
            break

    if messsage == 'borrado':
        print("Cliente eliminado correctamente.")
        flash("Cliente eliminado correctamente.")
    else:
        print("No se encontró el cliente")
        flash("No se encontró el cliente")

    with open('clientes.json', 'w') as file:
        json.dump(clientes, file, indent=4)
        

    return redirect(url_for('clientes_borrar'))

################################################################
@app.route('/clientes-pre-editar', methods=['POST', 'GET'])
def clientes_pre_editar():
    lista_pre_editar = [
        'Concesionario La Ñata',  # h1
        'Bienvenido!',  # h2
        'Editar Cliente',  # h3
        'Ingrese el ID del Cliente o Documento que desea editar',  # h4
        'Volver a Clientes',
    ]
    return render_template('clientes-pre-editar.html', lista_pre_editar=lista_pre_editar)

@app.route('/submit-pre-e-c', methods = ['POST', 'GET'])
def clientes_pre_editar_submit_form():
    global cliente_pre_editar

    form_data = request.form
    
    parametro = form_data.get('parametro')

    cliente_pre_editar = parametro

    print(cliente_pre_editar)

    return redirect(url_for('clientes_editar'))

@app.route('/clientes_editar', methods=['GET', 'POST'])
def clientes_editar():
    lista_editar = [
        'Concesionario La Ñata',  # h1
        'Bienvenido!',  # h2
        'Editar Cliente',  # h3
        'Ingrese los datos del Cliente que deseee editar',  # h4
        'Volver a Clientes',
    ]
    return render_template('clientes-editar.html', lista_editar=lista_editar)

@app.route('/submit-e-c', methods=['GET','POST'])
def clientes_editar_submit_form():

    with open('clientes.json', 'r') as file:
        clientes = json.load(file)

    form_data = request.form

    parametro = cliente_pre_editar 
 
    if parametro.isdigit(): #
        parametro = int(parametro)
        editar_por = 'item_id'
        
    else:
        parametro = cliente_pre_editar
        editar_por = 'patente'
        diccionario_a_editar = None

    for registro in clientes:
        if registro.get(editar_por) == parametro:
            diccionario_a_editar=registro
            break

    if not diccionario_a_editar:
        print("No se encontró el cliente")
        flash("No se encontró el cliente")
        return redirect(url_for('clientes_editar'))
    
    item_id = parametro

    if editar_por == 'documento':
        item_id = diccionario_a_editar['item_id']

    documento = form_data.get('documento') or diccionario_a_editar['documento']
    nombre = form_data.get('nombre') or diccionario_a_editar['nombre']
    apellido = form_data.get('apellido') or diccionario_a_editar['apellido']
    direccion = form_data.get('direccion') or diccionario_a_editar['direccion']
    telefono = form_data.get('telefono') or diccionario_a_editar['telefono']
    correo_electronico = form_data.get('correo_electronico') or diccionario_a_editar['correo_electronico']

    cliente_form = {
        'item_id': item_id,
        'nombre': nombre,
        'apellido': apellido,
        'documento': documento,
        'direccion': direccion,
        'telefono': telefono,
        'correo_electronico': correo_electronico,
    }

    print(cliente_form)

    for cliente in clientes:
        if cliente[editar_por] == parametro:
            cliente.update(cliente_form)
            break
    
    with open('clientes.json', 'w') as file:
        json.dump(clientes, file, indent=4)
        flash('Datos de cliente actualizados')

    return redirect(url_for('clientes_editar'))

@app.route('/clientes_editar', methods=['GET','POST'])
def cliente_editar():
    lista_editar = [
        'Concesionario La Ñata',  # h1
        'Bienvenido!',  # h2
        'Editar Cliente',  # h3
        'Ingrese los datos del Cliente',  # h4
        'Volver a Clientes',
    ]
    return render_template('clientes-editar.html', lista_editar=lista_editar)

#@app.route('/submit-e-c', methods=['GET','POST'])

def clientes_editar_submit_form():
    with open('clientes.json, r') as f:
        clientes = json.load(f)

    parametro = cliente_pre_editar

    if parametro.isdigit():
        parametro = 'item_id'
    else:
        parametro = clientes_pre_editar
        editar_por = 'patente'

    diccionario_a_editar = None

    for registro in clientes:
        if registro.get(editar_por) == parametro:
            diccionario_a_editar=registro
            break

    if not diccionario_a_editar:
        print('No se encontró el registro')
        return redirect(url_for('clientes'))
    
    item_id = parametro

    if editar_portal == 'patente':
        item_id = diccionario_a_editar.get['item_id']
    
    nombre = request.form.get('nombre') or diccionario_a_editar.get['nombre']
    apellido = request.form.get('apellido') or diccionario_a_editar.get['apellido']
    documento = request.form.get('documento') or diccionario_a_editar.get['documento']
    direccion = request.form.get('direccion') or diccionario_a_editar.get['direccion']
    telefono = request.form.get('telefono') or diccionario_a_editar.get['telefono']
    correo_electronico = request.form.get('correo_electronico') or diccionario_a_editar.get['correo_electronico']

    cliente_form = {
        'item_id': item_id,
        'nombre': nombre,
        'apellido': apellido,
        'documento': documento,
        'direccion': direccion,
        'telefono': telefono,
        'correo_electronico': correo_electronico,
    }

    print(cliente_form)

    for cliente in clientes:
        if cliente[editar_por] == parametro:
            vehiculo.update(cliente_form)
            break

    with open('clientes.json', 'w') as file:
        json.dump(clientes, file, indent=4)
    print("Cliente editado correctamente.")
    return redirect(url_for('clientes_editar'))

################################################################################
################################################################################
@app.route('/transacciones', methods=['GET', 'POST'])
def transacciones():
    lista_menu = [
    '1. Crear Transacción', 
    '2. Listar Transacciones',
    '3. Buscar Transacción', 
    '4. Volver al Menú Principal',
    'Menu Transacciones', #1
    'Ir al Menú',
    'Concesionario La Ñata',#h2
    'Bienvenido!'] #h2

   # opcion_menu_transacciones = request.form.get('opcion')

    return render_template('transacciones.html', **{'lista_menu': lista_menu})

@app.route('/transacciones-crear', methods=['GET', 'POST'])
def transaccion_crear():
    lista_crear = [
        'Concesionario La Ñata',  # h1
        'Bienvenido!',  # h2
        'Crear Transacción',  # h3
        'Ingrese los datos de la Transacción',  # h4
        'Volver a Transacciones',
    ]
    return render_template('transacciones-crear.html',lista_crear=lista_crear)

@app.route('/submit-c-t', methods=['POST','GET'])
def transaccion_crear_submit_form():

    with open ('transacciones.json', 'r') as file:
        transacciones = json.load(file)
        print(transacciones)
    
    form_data = request.form

    item_id = len(transacciones) + 1

    nueva_transaccion = {
        'item_id': item_id,
        'id_vehiculo': form_data.get('id_vehiculo'),
        'id_cliente': form_data.get('id_cliente'),
        'tipo_transaccion': form_data.get('tipo_transaccion'),
        'fecha': form_data.get('fecha'),
        'monto': form_data.get('monto'),
        'observaciones': form_data.get('observaciones'),
    }
    transacciones.append(nueva_transaccion)
    with open('transacciones.json', 'w') as file:
        json.dump(transacciones, file, indent=4)
    print("Transacción creada correctamente.")
    flash('Transacción creada correctamente.')

    return redirect(url_for('transacciones-crear'))



@app.route('/transacciones-listar', methods=['GET','POST'])
def listar_transacciones():
    
    #   Si existe el archivo, cargamos los datos en memoria
    with open('transacciones.json', 'r') as file:
        transacciones = json.load(file)
        #cargamos los datos de json en memoria
    
    lista_listar = [
        'Concesionario La Ñata',  # h1
        'Bienvenido!',  # h2
        'Listado de Transacciones',  # h3
        'Volver a Transacciones',
    ] 
    
    return render_template('transacciones-listar.html',lista_listar=lista_listar, transacciones=transacciones)


@app.route('/transacciones/buscar', methods=['GET', 'POST'])
def buscar_transacciones():
    if request.method == 'POST':
        tipo_transaccion = request.form['tipo_transaccion']
        criterio = request.form['criterio']
        valor = request.form['valor']

        with open('transacciones.json', 'r') as file:
            transacciones = json.load(file)

        if criterio == 'id_cliente':
            resultados = [t for t in transacciones if t['id_cliente'] == int(valor) and t['tipo_transaccion'] == tipo_transaccion]
        elif criterio == 'id_vehiculo':
            resultados = [t for t in transacciones if t['id_vehiculo'] == int(valor) and t['tipo_transaccion'] == tipo_transaccion]
        elif criterio == 'rango_fechas':
            fecha_desde, fecha_hasta = valor.split(',')
            resultados = [t for t in transacciones if fecha_desde <= t['fecha'] <= fecha_hasta and t['tipo_transaccion'] == tipo_transaccion]
        else:
            resultados = []

        return render_template('resultados_busqueda.html', transacciones=resultados)

    return render_template('buscar_transacciones.html')


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

    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M")

    headers = ['Dolar Promedio','Dolar Venta','Dolar Compra']
    fields1 = [blue_string]  # Dólar Blue
    fields2 = [oficial_string]  # Dólar Oficial
        
    return render_template('cotizacion.html', **{'lista_menu': lista_menu, 'headers': headers, 'fields1':fields1, 'fields2':fields2, 'formatted_date':formatted_date})

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

if __name__ == '__main__':
    app.run(debug=True)