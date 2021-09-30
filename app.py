from flask import Flask, request, jsonify
import random

#CLASES
class Cliente:
    name = ""
    last_name = ""
    identificacion = 0

    def __init__(self,name, last_name,identificacion):
        self.name = name
        self.last_name = last_name
        self.identificacion = identificacion
    
    def getName(self):
        return self.name

    def getLast_name(self):
        return self.last_name

    def setName(self,newName):
        self.name = newName
    
    def setLast_name(self,newLast_name):
        self.last_name = newLast_name

    def getIdentificacion(self):
        return self.identificacion

    def setIdentificacion(self,newId):
        self.identificacion = newId

#METODOS   
def generar_cod():
    return random.randint(1,2000)

def buscar_cliente(id_cliente):
    global clientes
    estado = False
    contador = 0
    while(contador < len(clientes) and estado == False):
        if clientes[contador][0] == id_cliente:
            estado = True
        contador+=1
    return estado

def retornar_cliente(id_cliente):
    global clientes
    estado = False
    contador = 0
    dato = ""
    while(contador < len(clientes) and estado == False):
        if clientes[contador][0] == id_cliente:
            estado = True
            dato = clientes[contador]
        contador+=1
    return dato

app = Flask(__name__)
clientes = []
inventario = []
compras = {}
contador_compra = 0
total = 0

@app.route("/apis/clientes", methods=["POST"])
def cliente():
    global clientes
    resp = ""
    est = False
    codigo = 0
    json = request.get_json()
    """ Return a friendly HTTP greeting. """
    name = json["name"]
    last_name = json["last_name"]
    while(est == False):
        if(buscar_cliente(generar_cod)== False):
            codigo = generar_cod()
            est = True
    user = Cliente(name,last_name,codigo)
    clientes.append([user.getIdentificacion(),user.getName(),user.getLast_name()])
    #print(str(user.getIdentificacion() + " "+ user.getName()))
    for x in clientes:
        resp += str(x[0])+","
    respuesta = {"CLIENTES": f"{resp}"}
    return jsonify(respuesta)

@app.route("/apis/productos", methods=["POST"])
def productos():
    global total
    global contador_compra
    global clientes
    global inventario
    aux = []
    """ Return a friendly HTTP greeting. """
    result =""
    respuesta = {}
    json = request.get_json()
    productos = json["productos"]
    id_cliente = json["id_cliente"]
    if (buscar_cliente(id_cliente)):
        for x in productos:
            aux.append([x["prod_id"],x["nombre_proc"],x["valor"]])
            total += x["valor"]
        respuesta = {"Cuenta": f"cuenta con codigo {contador_compra} se registro exitosamente"}
        compras[contador_compra]=[aux.copy(),total,retornar_cliente(id_cliente)]
        inventario.append(aux.copy())
        contador_compra+=1
        total = 0
    else:
        respuesta = {"Respuesta": f"el usuario con codigo {id_cliente} no existe"}
    return jsonify(respuesta)

@app.route("/apis/compra", methods=["POST"])
def compra():
    global compras
    """ Return a friendly HTTP greeting. """
    respuesta = {}
    json = request.get_json()
    codigo_compra = json["codigo_compra"]
    if (codigo_compra in compras):
         respuesta = {"Informacion": f"la informacion de la compra con codigo {codigo_compra} es : "+
                                        f"{compras[codigo_compra][0]}   Total: ${compras[codigo_compra][1]}  "
                                        + f"Cliente: {compras[codigo_compra][2]}"}
    else:
        respuesta = {"Respuesta": f"la compra con codigo {codigo_compra} no existe"}
    return jsonify(respuesta)



if __name__ == "__main__":
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host="localhost", port=8080, debug=True)