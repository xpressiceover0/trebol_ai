# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional

#Modelo de Registro
class SolicitudModel(BaseModel):
    registro_id: str = Field(..., max_length=10)
    nombre: str = Field(..., min_length=1, max_length=20, regex="[A-Za-z\s]{2,20}")
    apellido: str = Field(..., min_length=1, max_length=20, regex="[A-Za-z\s]{2,20}")
    edad: int = Field(..., gt=0, lt=100)
    afinidad: int = Field(...)

class RegistroQuery(BaseModel):
    registro_id: Optional[str] = Field(default=None, max_length=10)
    nombre: Optional[str] = Field(default=None, min_length=1,max_length=20, regex="[A-Za-z\s]{2,20}")
    apellido: Optional[str] = Field(default=None, min_length=1,max_length=20, regex="[A-Za-z\s]{2,20}")
    edad: Optional[int] = Field(default=None,  gt=0, lt=100)
    afinidad: Optional[int] = Field(default=None)

class SignInModel(BaseModel):
    username: str = Field(..., min_length=5,max_length=20)
    password:str = Field(..., min_length=8,max_length=20)
    nombre:str =Field(..., max_length=40)

# Modelo de Usuario de la plataforma
class LoginModel(BaseModel):
    username: str = Field(..., min_length=5,max_length=20)
    password: str = Field(..., min_length=8, max_length=20)