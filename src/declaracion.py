from tkinter.tix import INTEGER
from tokenize import String
from turtle import circle


from tkinter import *


class Cliente:
    def __init__(self, name, ci, dir):
        self.nombre = name
        self.ruc = ci
        self.direccion = dir

    # def __init__(self):
    #     self.nombre = "No name"
    #     self.ruc = "XXXXXXX"
    #     self.direccion = ""


class Producto:
    def __init__(self, monto1, monto2, name, x, cod, id):
        self.pc = monto1
        self.pv = monto2
        self.nombre = name
        self.cantidad = x
        self.codigo = cod
        self.id = id


class Cajero:
    def __init__(self, name, ci):
        self.nombre = name
        self.ruc = ci


class TipoProducto(object):
    def __init__(self, name, monto, cantidad, codigo):
        self.nombre = name
        self.precio = monto
        self.cantidad = cantidad
        self.codigo = codigo
