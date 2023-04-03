# -*- coding: utf-8 -*-
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import String,DateTime,SmallInteger
from config.db import meta, engine

# PROFESORES USUARIOS DE LA PLATAFORMA =============================================================================================
profesoresdb=Table("profesoresdb",meta,
    Column("id", String(32), primary_key=True), # validación y agragacion de tablas dependientes
    Column("creacion", DateTime), # informacion de la fecha de alta
    Column("nombre", String(40), unique=True), # informacion y uso en mensajes y promociones como dato payload
    Column("username", String(20), unique=True), # login y registro
    Column("password", String(20)), # login y registro
    Column("activo", SmallInteger)) # validacion de uso de la plataforma


# TODOS LOS REGISTROS (aceptados y prospectos) ========================================================================================
registrosdb=Table("registrosdb",meta,
    Column("id", String(10), primary_key=True), #La persona debe tener un único telefono al que llegaran sus notificaciones. No hay mas de una persona con el mismo telefono
    Column("creacion", DateTime), # informacion de la fecha de registro
    Column("nombre", String(20)), # nombre(s) del registrado
    Column("apellido", String(20)), #  apellidos del registrado
    Column("edad", SmallInteger), # Edad hasta 99 años
    Column("afinidad", SmallInteger),# tipo de afinidad magica
    Column("aceptado", SmallInteger)) #estatus de espera(0), aceptado(1) o rechazado(-1)


# ESTUDIANTES ===========================================================================================================
estudiantesdb=Table("estudiantesdb",meta,
    Column("id", String(32), primary_key=True),# identificador unico del registro
    Column("creacion", DateTime), # fecha en que fue aceptado como estudiante
    Column("registro_id",String(10), ForeignKey("registrosdb.id")), # registro de estudiante
    Column("grimorio_id", String(2), ForeignKey("grimoriosdb.id")), # grimorio al que pertenece
    Column("activo", SmallInteger)) # si está activo(1), inactivo(0) o suspendido(-1)


# GRIMORIOS ========================================================================================
grimoriosdb=Table("grimoriosdb",meta,
    Column("id", String(2), primary_key=True), # id del grimorio
    Column("grimorio", String(20)), # nombre del grimorio
    Column("trebol", SmallInteger)) # numero de hojas del trebol


# AFINIDAD ========================================================================================
afinitydb=Table("afinitydb",meta,
    Column("id", String(2), primary_key=True), # id numerico de la afinidad
    Column("afinidad", String(20))) # nombre de la afinidad

meta.create_all(engine)
