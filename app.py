
from flask import Flask,jsonify,request,render_template,Response

import json 
from functions import todosProductos,limite_producto
import requests 
app = Flask(__name__)

@app.route('/mercadoLibre',methods=["GET"])
def mercadoLibre():
    data = json.loads(request.data)
    print(data)
    if 'limite' not in data:
        titulos,urls,precios = todosProductos(data["producto"])
    else:
        titulos,urls,precios = limite_producto(data["producto"],data["limite"])
    return jsonify({"datos":{"titulos":titulos,"urls":urls,"precios":precios}})
@app.route('/descargarInfo',methods=["GET","POST"])
def descargarInfo():
    if request.method=="POST":
        print("hola")
        producto = request.form["producto"]
        limite = request.form["limite"]
        r = requests.get('http://localhost:5000/mercadoLibre',json={"producto":producto,"limite":int(limite)})
        print(r.status_code)
        if r.status_code==200:
            data = json.loads(r.text)
           
            t = ""
            for i,j,z in zip(data["datos"]["titulos"],data["datos"]["precios"],data["datos"]["urls"]):
                t+=f"{i}|{j}|{z}\n"
            
            return Response(
                t,
                mimetype="text",
                headers={
                    "Content-disposition":"attachment; filename=datos.txt"
                }
            )
        return "ERROR"
        pass
    return render_template('index.html')




if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)