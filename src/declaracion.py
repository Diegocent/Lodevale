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
    def __init__(self, monto1, monto2, name, x, cod):
        self.pc = monto1
        self.pv = monto2
        self.nombre = name
        self.cantidad = x
        self.codigo = cod


class Cajero:
    def __init__(self, name, ci):
        self.nombre = name
        self.ruc = ci


class TipoProducto(object):
    def __init__(self, name, monto, cantidad, codigo, id):
        self.nombre = name
        self.precio = monto
        self.cantidad = cantidad
        self.codigo = codigo
        self.id = id


# usar el id de esa venta para guardarlo en descripcion e ir insertando producto por producto siempre con el mismo id de venta

# para hacer la busqueda se trae todos los registros desde la ultima fecha y se trae
