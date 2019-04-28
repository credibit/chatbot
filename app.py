# coding: utf8
import os
import json
import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from information import existeMarca, getEngines, existeModelo, existeSubmodelo, existeMotor, getPrice, js_read,js_read2, js_save,js_save2, existeParte, getCart, submitCart, getSubModels
import requests
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
CORS(app)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

account_sid = 'ACa9513b791536c7a97c306e8f9b6c9a79'
auth_token = '07c24096e11336cd33017101119f72e0'
account_sid2 = 'AC01310a6100555a897c5e4cf36f4bc601'
auth_token2 = '5be98f5de25583f76a5e1354f6bd442d'
client = Client(account_sid, auth_token)
client2 = Client(account_sid2, auth_token2)
#from models import Usuarios

@app.route("/")
def hello():
    return "API of the team BeMyGuide at Bosch Hackathon TalentLand 2019"

@app.route("/palomino", methods=['POST','GET'])
def palomitas():
    valor=request.args
    print("sirvee")
    print(valor)
    return "jeje"


@app.route("/sms", methods=['POST'])
def wazza():
    msg = request.form.get('Body')
    resp = MessagingResponse()
    parametros={"mensaje":msg}
    dic=js_read2()
    if("siguiente" not in dic):
        dic["siguiente"]="saludo"
    siguiente=dic["siguiente"]
    print("dicc")
    print(dic)
    print("---")
    url="http://gotaroja.com:5000/creditEligibility"
    #temp={'ingresoNeto': 4200, 'ingresoMensual': 21000, 'cantidadDeseada': 20000, 'puntosBuro': 90, 'plazoDeseado': 6, 'puntosSat': 75, 'nombreEmpresa': 'zubut', 'correo': 'luis@zubut.com', 'companySite': 'https://zubut.com'}
    #r=requests.post(url, json=temp)
    #print("////////")
    #print(r.json())
    #msg="bye"
    if(msg=="bye"):
        toSend="Bye!"
        resp.message("{}".format(toSend))
        dic={}     
        js_save2(dic)
        return str(resp)
    if(siguiente=="saludo"):
        toSend="Hola! ¿En que te puedo ayudar?"
        dic["siguiente"]="conseguir_datos"
    elif(siguiente=="conseguir_datos"):
        toSend="¿Cual es el nombre de tu empresa?"
        resp.message("{}".format(toSend))
        toSend="Claro, solo tienes que contestar unas preguntas"
        dic["siguiente"]="nombreEmpresa"
    elif(siguiente=="nombreEmpresa"):
        dic["nombreEmpresa"]=msg
        toSend="¿Cual es el la pagina web de tu empresa?"
        dic["siguiente"]="urlEmpresa"
    elif(siguiente=="urlEmpresa"):
        dic["urlEmpresa"]=msg
        toSend="¿Cual es el correo de tu empresa?"
        dic["siguiente"]="correoEmpresa"
    elif(siguiente=="correoEmpresa"):
        dic["correoEmpresa"]=msg
        print("ADDING EMAIL")
        print(dic)
        toSend="Okay. ¿Cuantos puntos de buro tiene?"
        dic["siguiente"]="puntosBuro"
    elif(siguiente=="puntosBuro"):
        dic["puntosBuro"]=msg
        toSend="Bien. ¿Cuanto spuntos del SAT tiene?"
        dic["siguiente"]="puntosSat"
    elif(siguiente=="puntosSat"):
        dic["puntosSat"]=msg
        toSend="Excelete. ¿Cual es tu ingreso mensual?"
        dic["siguiente"]="ingresoMensual"
    elif(siguiente=="ingresoMensual"):
        dic["ingresoMensual"]=msg
        toSend="¿Cual es tu ingreso neto?"
        dic["siguiente"]="ingresoNeto"
    elif(siguiente=="ingresoNeto"):
        dic["ingresoNeto"]=msg
        toSend="¿Cual es el monto deseado?"
        dic["siguiente"]="montoDeseado"
    elif(siguiente=="montoDeseado"):
        dic["montoDeseado"]=msg
        toSend="Y finalmente, ¿A cuántos meses te gustaria tu credito?"
        dic["siguiente"]="plazoDeseado"
    elif(siguiente=="plazoDeseado"):
        dic["plazoDeseado"]=msg
        toSend="Analizando datos..."
        resp.message("{}".format(toSend))
        toSend="ANALIZADO wii..."
        print("antes de")
        print(dic)
        parametros={
            "nombreEmpresa": dic["nombreEmpresa"],
            "correo": dic["correoEmpresa"], 
            "puntosBuro": int(dic["puntosBuro"]), 
            "puntosSat": int(dic["puntosSat"]), 
            "ingresoMensual": int(dic["ingresoMensual"]), 
            "ingresoNeto": int(dic["ingresoNeto"]), 
            "cantidadDeseada": int(dic["montoDeseado"]),
            "plazoDeseado": int(dic["plazoDeseado"]),
            "companySite": dic["urlEmpresa"]
        }
        print("se manda")
        print(parametros)
        r=requests.post(url, json=parametros)
        print("////////")
        print(r.json())
        valid=r.json()["is_valid"]
        if(valid):
            toSend="Hemos encontrado una opcion para ti: \n"        
            pagar=""
            meses=r.json()["months"]
            cantidad=r.json()["ammount"]
            for element in meses:
                pagar+=str(element)+", "
            toSend+="Puedes pagar a : "+pagar +" meses\n"
            toSend+="Y tendras que pagar un total de "+str(cantidad)+"\n"
            toSend+="\n"
            toSend+="Para saber mas visitanos en https://konfio.com"
            print(meses)
            print(cantidad)
        else:
            toSend="No se te ha podido autorizar un credito"
        dic={}     
    js_save2(dic)
    resp.message("{}".format(toSend))
    return str(resp)

@app.route("/messenger", methods=['POST'])
def wazza2():
    msg = request.form.get('Body')
    resp = MessagingResponse()
    parametros={"mensaje":msg}
    dic=js_read2()
    if("siguiente" not in dic):
        dic["siguiente"]="saludo"
    siguiente=dic["siguiente"]
    print("dicc")
    print(dic)
    print("---")
    url="http://gotaroja.com:5000/creditEligibility"
    #temp={'ingresoNeto': 4200, 'ingresoMensual': 21000, 'cantidadDeseada': 20000, 'puntosBuro': 90, 'plazoDeseado': 6, 'puntosSat': 75, 'nombreEmpresa': 'zubut', 'correo': 'luis@zubut.com', 'companySite': 'https://zubut.com'}
    #r=requests.post(url, json=temp)
    #print("////////")
    #print(r.json())
    #msg="bye"
    if(msg=="bye"):
        toSend="Bye!"
        resp.message("{}".format(toSend))
        dic={}     
        js_save2(dic)
        return str(resp)
    if(siguiente=="saludo"):
        toSend="Hola! ¿En que te puedo ayudar?"
        dic["siguiente"]="conseguir_datos"
    elif(siguiente=="conseguir_datos"):
        toSend="¿Cual es el nombre de tu empresa?"
        resp.message("{}".format(toSend))
        toSend="Claro, solo tienes que contestar unas preguntas"
        dic["siguiente"]="nombreEmpresa"
    elif(siguiente=="nombreEmpresa"):
        dic["nombreEmpresa"]=msg
        toSend="¿Cual es el la pagina web de tu empresa?"
        dic["siguiente"]="urlEmpresa"
    elif(siguiente=="urlEmpresa"):
        dic["urlEmpresa"]=msg
        toSend="¿Cual es el correo de tu empresa?"
        dic["siguiente"]="correoEmpresa"
    elif(siguiente=="correoEmpresa"):
        dic["correoEmpresa"]=msg
        print("ADDING EMAIL")
        print(dic)
        toSend="Okay. ¿Cuantos puntos de buro tiene?"
        dic["siguiente"]="puntosBuro"
    elif(siguiente=="puntosBuro"):
        dic["puntosBuro"]=msg
        toSend="Bien. ¿Cuanto spuntos del SAT tiene?"
        dic["siguiente"]="puntosSat"
    elif(siguiente=="puntosSat"):
        dic["puntosSat"]=msg
        toSend="Excelete. ¿Cual es tu ingreso mensual?"
        dic["siguiente"]="ingresoMensual"
    elif(siguiente=="ingresoMensual"):
        dic["ingresoMensual"]=msg
        toSend="¿Cual es tu ingreso neto?"
        dic["siguiente"]="ingresoNeto"
    elif(siguiente=="ingresoNeto"):
        dic["ingresoNeto"]=msg
        toSend="¿Cual es el monto deseado?"
        dic["siguiente"]="montoDeseado"
    elif(siguiente=="montoDeseado"):
        dic["montoDeseado"]=msg
        toSend="Y finalmente, ¿A cuántos meses te gustaria tu credito?"
        dic["siguiente"]="plazoDeseado"
    elif(siguiente=="plazoDeseado"):
        dic["plazoDeseado"]=msg
        toSend="Analizando datos..."
        resp.message("{}".format(toSend))
        toSend="ANALIZADO wii..."
        print("antes de")
        print(dic)
        parametros={
            "nombreEmpresa": dic["nombreEmpresa"],
            "correo": dic["correoEmpresa"], 
            "puntosBuro": int(dic["puntosBuro"]), 
            "puntosSat": int(dic["puntosSat"]), 
            "ingresoMensual": int(dic["ingresoMensual"]), 
            "ingresoNeto": int(dic["ingresoNeto"]), 
            "cantidadDeseada": int(dic["montoDeseado"]),
            "plazoDeseado": int(dic["plazoDeseado"]),
            "companySite": dic["urlEmpresa"]
        }
        print("se manda")
        print(parametros)
        r=requests.post(url, json=parametros)
        print("////////")
        print(r.json())
        valid=r.json()["is_valid"]
        if(valid):
            toSend="Hemos encontrado una opcion para ti: \n"        
            pagar=""
            meses=r.json()["months"]
            cantidad=r.json()["ammount"]
            for element in meses:
                pagar+=str(element)+", "
            toSend+="Puedes pagar a : "+pagar +" meses\n"
            toSend+="Y tendras que pagar un total de "+str(cantidad)+"\n"
            toSend+="\n"
            toSend+="Para saber mas visitanos en https://konfio.com"
            print(meses)
            print(cantidad)
        else:
            toSend="No se te ha podido autorizar un credito"
        dic={}     
    js_save2(dic)
    resp.message("{}".format(toSend))
    return str(resp)

if __name__ == '__main__':
    app.run()