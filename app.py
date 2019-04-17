from flask import Flask, render_template, request, flash
import redis
import json
import random

app = Flask(__name__)
app.secret_key = 'my_secret_key'
reservadas = []



def connect_db():
    '''Crear conexion a base de datos'''
    conexion = redis.StrictRedis(host='127.0.0.1', port=6379, db=2, decode_responses=True)
    if(conexion.ping()):
        print ("conectado al servidor de redis")
    else:
        print("Error en la conexion a redis")
    return conexion



@app.route('/', methods=['GET', 'POST'])
def home():

    rdb = connect_db()

    keys = []
    keys = rdb.keys(pattern="*")

   
    
    entradas = []
#    resevada = []
    
    for llave in keys:
        entrada = [llave, rdb.lrange(llave, 0, -1)]
        entradas.append(entrada)
    

    
    print(entradas)
    # rdb.lpush(id, 'Nombre', 'estado', precio)
    if(request.method == 'GET'):
        
        
        print(entradas)
        
        return render_template('/index.html', entradas = entradas)
    
    
    if (request.method == 'POST'):
        llave = request.form['llave']
        entrada = request.form['entrada']
        precio = request.form['precio']
        
        
        rdb.lset(llave, 1, 'Reservado')
        #llave +=1
        #rdb.setex(llave, 10, 'Reservado')
        
        
    

        return render_template('/index.html', entradas = entradas)

    
@app.route('/cargarticket', methods=['GET', 'POST'])
def cargarticket():
    rdb = connect_db()
    if (request.method == 'POST'):
        nombreEntrada = (request.form['entrada'])
        precio = (request.form['precio'])

        rdb.lpush(random.randint(10000, 99999), nombreEntrada, 'Disponible', precio)
        success_message = 'Entrada guardada correctamente'
        flash(success_message)
        
        return render_template('/cargar-ticket.html')

    if (request.method  == 'GET'):
        return render_template('/cargar-ticket.html')


@app.route('/comprarentrada/<entrada>', methods=['GET', 'POST'])
def pagarticket(entrada):
    rdb = connect_db()

    if (request.method == 'GET'):
        valorEntrada = rdb.lrange(entrada, 0, -1)
        
        #if(rdb.ttl(entrada) <= 0):

          #  rdb.lpush(entrada, valorEntrada[2], 'Disponible', valorEntrada[0])
         #   print('La reserva ha expirado: '+ entrada)
        #entrada -=1    

        return render_template('/comprar-ticket.html', entrada = valorEntrada, id = entrada)


    if (request.method == 'POST'):
        keys = []
        keys = rdb.keys(pattern="*")
            
        entradas = []
        
        id = request.form['id']
        entrad = request.form['entrada']
        precio = request.form['precio']

        rdb.lset(id, 1, 'Vendido')
        

        for llave in keys:
            entrada = [llave, rdb.lrange(llave, 0, 2)]
            entradas.append(entrada)
            
        

        return render_template('/index.html', entradas = entradas)



if (__name__ == '__main__'):
    app.run(host='localhost', port=5000, debug=False)