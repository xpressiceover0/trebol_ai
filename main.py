# -*- coding: utf-8 -*-
import uvicorn
#import fastapi
from typing import  List
#import secrets
from datetime import datetime
import uuid
import random as rnd

#Models
from classmodels.models import *

#fastAPI
from fastapi import FastAPI, Body, Query, Path, Header #, Depends
from fastapi.middleware.cors import CORSMiddleware

'''
#Auth
from auth.authjwt import signJWT, decodeJWT, JWTBearer
#from decouple import config
'''

#Database
from config.db import conn
from schemas.dbtables import profesoresdb, registrosdb, estudiantesdb, grimoriosdb, afinitydb
from sqlalchemy import text


#API CONFIGURATION------------------------------------------------------------------------------
#=================================================================================
app=FastAPI()

#CORS
app.add_middleware(CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'])

#________________________________________________________________________________________________

#HOME ====================================================================================
@app.get("/")
async def home():
    return "Escuela del reino del trebol"

# SESIONES ====================================================================================
@app.post("/login", tags=["Profesores"]) 
async def loginuser(user: LoginModel = Body(...)):

    resp=conn.execute(profesoresdb.select().where(profesoresdb.c.username==user.username)).first()
    
    if resp:

        id, _ ,nombre, _ ,password,activo = resp
    
        if password==user.password:
            if activo==1:
                return {"msg":f"Bienvenido profesor {nombre}.", "profesor_id": id, "check":"true"}
            else:
                return {"msg":"Tu estatus de profesor esta inactivo.Revisa con el Rey Mago tu estatus para poder continuar.", "check":"false"}
    else:
        return {"msg": "Usuario incorrecto o inexistente", "check":"false"}

@app.post("/signin", tags=["Profesores"]) 
async def signprofesor(signinmodel: SignInModel = Body(...)):
    # se genera un nuevo registro que será insertado en la base de datos
    nuevo_profesor={
        "id":uuid.uuid4().hex,
        "creacion":datetime.now(),
        "nombre":signinmodel.nombre,
        "username":signinmodel.username,
        "password":signinmodel.password,
        "activo": 1}
    
    resp=conn.execute(profesoresdb.select().where(profesoresdb.c.username==signinmodel.username)).first()

    if not resp:
        conn.execute(profesoresdb.insert().values(nuevo_profesor))
        conn.commit()

        return {"msg": "Usuario creado con exito", "check":"true"}
    else:
        return {"msg": "El usuario que intenta utilizar ya existe", "check":"false"}


# PARA ASPIRANTES ====================================================================================

# CREACION DE NUEVO REGISTRO CON TODOS LOS DATOS REQUERIDOS DEL SOLICITANTE
@app.post("/solicitudes", tags=["Aspirantes"])
async def enviar_solicitud(solicitud: SolicitudModel=Body(...)):
    
    # se genera un nuevo registro que será insertado en la base de datos
    nuevo_registro={
        "id":solicitud.registro_id,
        "creacion":datetime.now(),
        "nombre":solicitud.nombre,
        "apellido":solicitud.apellido,
        "edad":solicitud.edad,
        "afinidad": solicitud.afinidad,
        "aceptado": 0}
    
    resp=conn.execute(registrosdb.select().where(
        registrosdb.c.nombre==solicitud.nombre, 
        registrosdb.c.apellido==solicitud.apellido, 
        registrosdb.c.aceptado!=0)).first()
    
    if resp:
        id,aceptado = resp[0], resp[-1]
        if aceptado == -1:
            
            # actualizacion de registro que ya ha sido previamente 
            conn.execute(registrosdb.update(registrosdb.c.id == id).values(
                creacion=datetime.now(), edad=solicitud.edad, afinidad=solicitud.afinidad, aceptado=0 ))
            
            conn.commit()
            
            return {"msg": "Usted tiene un registro previo. Se ha generado una nueva solicitud sobre su registro.", 
                    "check":"true", 
                    "id_registro":id}
        
        elif aceptado == 1:
            return {"msg": "Usted ya ha sido aceptado.", 
                    "check":"true", 
                    "id_registro": id}

    
    else:
        # insercion de registro
        conn.execute(registrosdb.insert().values(nuevo_registro))
        conn.commit()

        return {"msg": "Se ha generado una nueva solicitud de registro.", 
                "check":"true",
                "id_registro":nuevo_registro["id"]}


# ACUTALIZACION DE UN REGISTRO YA EXISTENTE POR PARTE DEL SOLICITANTE
@app.put("/solicitudes/{id_registro}", tags=["Aspirantes"])
async def actualizar_solicitud(id_registro: str = Path(...), registroquery: RegistroQuery=Body(...)):
    
    registro_editado={}

    resp=conn.execute(registrosdb.select().where(registrosdb.c.id == id_registro, registrosdb.c.aceptado == 0)).first()
    
    if not resp:
        return {"msg": "Tu numero de registro ya ha sido procesado o es incorrecto", "check":"false"}

    if registroquery.nombre:
        registro_editado["nombre"]=registroquery.nombre
    if registroquery.apellido:
        registro_editado["apellido"]=registroquery.apellido
    if registroquery.edad:
        registro_editado["edad"]=registroquery.edad
    if registroquery.afinidad:
        registro_editado["afinidad"]=registroquery.afinidad
    
    conn.execute(registrosdb.update().filter(registrosdb.c.id==id_registro, registrosdb.c.aceptado==0).values(registro_editado))
    conn.commit()

    return {"msg": "Exito", "id_registro":id_registro, "check":"true"}
    
# VER DATOS DEL REGISTRO POR PARTE DE UN SOLICITANTE CON SU RESPECTIVO ID
@app.get("/solicitudes/{id_registro}", tags=["Aspirantes"])
async def consultar_solicitudes(id_registro: str = Path(...)):
    
    resp=conn.execute(registrosdb.select().where(registrosdb.c.id == id_registro)).first()
    
    if not resp:
        return {"msg": "Numero de registro incorrecto o inexistente", "check":"false"}
    
    return {"msg": "Exito", "payload": str(resp)}


# BORRAR SOLICITUD DE REGISTRO POR PARTE DE UN SOLICITANTE
@app.delete("/solicitudes/{id_registro}", tags=["Aspirantes"])
async def eliminar_solicitud(id_registro: str = Path(...)):
    
    resp=conn.execute(registrosdb.select().where(registrosdb.c.id == id_registro)).first()
    
    if not resp:
        return {"msg": "Numero de registro incorrecto o inexistente", "check":"false"}
    
    conn.execute(registrosdb.delete().where(registrosdb.c.id==id_registro))
    conn.commit()
    return {"msg": "Registro borrado", "id_registro":id_registro, "check":"true"}    




# PARA PROFESORES ====================================================================================

# VER TODOS LOS REGISTROS 
@app.get("/registros", status_code=200, tags=["Profesores"]) #, dependencies=[Depends(JWTBearer(()))])
async def ver_registros(profesor_id = Header(...)):
    
    #decoded_token=decodeJWT(authorization.replace("Bearer ",""))
    #profesor_id=decoded_token["profesor_id"]
    
    resp=conn.execute(profesoresdb.select().where(profesoresdb.c.id==profesor_id)).first()
    activo=resp[-1]
    if activo==1:
        payload=conn.execute(registrosdb.select()).fetchall()
        return {"msg": "Exito", "payload": str(payload), "check":"true"}
    
    else:
        return {"msg":"No tiene autorización para ver los registros.", "check":"false"}



# VER TODAS LAS SOLICITUDES DE INGRESO
@app.get("/registros/aspirantes", status_code=200 ,tags=["Profesores"])#, dependencies=[Depends(JWTBearer(()))])
async def registros_aspirantes(profesor_id = Header(...)):
    
    #decoded_token=decodeJWT(authorization.replace("Bearer ",""))
    #profesor_id=decoded_token["profesor_id"]
    
    resp=conn.execute(profesoresdb.select().where(profesoresdb.c.id==profesor_id)).first()
    
    activo = resp[-1]
    
    if activo==1:
        
        payload=conn.execute(registrosdb.select().where(registrosdb.c.aceptado==0)).fetchall()

        return {"msg": "Exito", "payload": str(payload), "check":"true"}
    
    else:
        return {"msg":"No tiene autorización para ver los registros.", "check":"false"}



# ASIGNAR ESTATUS DE ACEPTACION A LAS SOLICITUDES DE INGRESO INDICADAS
@app.post("/registros/aspirantes", status_code=201, tags=["Profesores"]) #,dependencies=[Depends(JWTBearer(()))])
async def registros_aspirantes(profesor_id = Header(...), aceptados: List[str] = Body(default=None), rechazados: List[str] = Body(default=None)):
    
    #decoded_token=decodeJWT(authorization.replace("Bearer ",""))
    #profesor_id=decoded_token["profesor_id"]
    
    resp=conn.execute(profesoresdb.select().where(profesoresdb.c.id==profesor_id)).first()
    activo=resp[-1]
    if activo==0:
        return {"msg":"No tiene autorización para ver los registros.", "check":"false"}
    if aceptados:
        conn.execute(registrosdb.update().filter(registrosdb.c.id.in_(aceptados), registrosdb.c.aceptado==0).values(aceptado=1))
        nuevos_estudiantes=[]

        for id_registro in aceptados:
            nuevos_estudiantes.append(
                {
                    "id": uuid.uuid4().hex, 
                    "creacion": datetime.now(), 
                    "registro_id": id_registro, 
                    "grimorio_id": rnd.choice(range(5)), 
                    "activo": 1
                })
        
        conn.execute(estudiantesdb.insert().values(nuevos_estudiantes))
    
    if rechazados: 
        conn.execute(registrosdb.update().filter(registrosdb.c.id.in_(rechazados), registrosdb.c.aceptado==0).values(aceptado=-1))
    
    
    conn.commit()
    return {"msg":"Se han efectuado los cambios", "check":"true"}



# VER A TODOS LOS ESTUDIANTES QUE YA HAN SIDO ASIGNADOS A UN GRIMORIO
@app.get("/estudiantes", status_code=200, tags=["Profesores"]) #, dependencies=[Depends(JWTBearer(()))])
async def consultar_estudiantes(profesor_id = Header(...)):
    
    #decoded_token=decodeJWT(authorization.replace("Bearer ",""))
    #profesor_id=decoded_token["profesor_id"]
    
    resp=conn.execute(profesoresdb.select().where(profesoresdb.c.id==profesor_id)).first()
    activo=resp[-1]
    
    if activo==1:
        q="SELECT estudiantesdb.*, grimoriosdb.grimorio, grimoriosdb.trebol FROM estudiantesdb"\
            " INNER JOIN grimoriosdb ON estudiantesdb.grimorio_id = grimoriosdb.id ORDER BY estudiantesdb.creacion DESC"
        
        payload = conn.execute(text(q)).fetchall()
        
        return {"msg": "Exito", "payload": str(payload), "check":"true"}
    
    else:
        return {"msg":"No tiene autorización para ver los grimorios.", "check":"false"}


# ACUTALIZACION DEL ESTATUS DE UN ALUMNO YA EXISTENTE POR PARTE DEL PROFESOR
@app.put("/estudiantes/{id_estudiante}", status_code=201, tags=["Profesores"]) #, dependencies=[Depends(JWTBearer(()))])
async def actualizar_solicitud(profesor_id = Header(...), id_estudiante: str = Path(...), estatus: int = Query(...)):
    
    #decoded_token=decodeJWT(authorization.replace("Bearer ",""))
    #profesor_id=decoded_token["profesor_id"]
    
    resp=conn.execute(profesoresdb.select().where(profesoresdb.c.id==profesor_id)).first()
    activo=resp[-1]
    if activo==1:
        resp=conn.execute(estudiantesdb.select().where(estudiantesdb.c.id == id_estudiante)).first()
        
        if not resp:
            return {"msg": "El numero de estudiante es incorrecto", "check":"false"}
        
        conn.execute(estudiantesdb.update().filter(estudiantesdb.c.id==id_estudiante).values(activo=estatus))
        conn.commit()

        return {"msg": "Estatus del estudiante actualizado", "id_estudiante":id_estudiante, "check":"true"}
    
    else:
        return {"msg":"No tiene autorización para editar a los estudiantes.", "check":"false"}


# SERVIDOR
if __name__=='__main__':
    
    resp=conn.execute(grimoriosdb.select()).fetchall()
    if not resp:
        crear_grimorios=[]
        

        grimorios=enumerate(["Sinceridad", "Esperanza", "Amor", "Buena Fortuna", "Desesperacion"])
        for i in grimorios:
            crear_grimorios.append(
                {"id":i[0],"grimorio": i[1], "trebol":i[0]+1}
            )
        
        conn.execute(grimoriosdb.insert().values(crear_grimorios))
    
    resp=conn.execute(afinitydb.select()).fetchall()
    if not resp:
        crear_afinidades=[]

        afinidades=enumerate(["Oscuridad", "Luz", "Fuego", "Agua", "Viento", "Tierra"])
        for i in afinidades:
            crear_afinidades.append({"id":i[0], "afinidad": i[1]})
        
        conn.execute(afinitydb.insert().values(crear_afinidades))
    conn.commit()

    uvicorn.run(app, host='0.0.0.0', port=8000)
