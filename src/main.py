from tkinter import *
from SiVentas import *
from declaracion import *
from datetime import datetime


# nombre = input()
# cedula = input()
# direccion = input()
# cliente = Cliente(nombre,cedula, direccion)
# ci=cliente.ruc
# nomcliente=cliente.nombre

root = Tk()
root.title("En lo de Vale sistem")
root.geometry("1500x800")
# root.iconbitmap(
#     "C:\\Users\\USER\\Desktop\\Lo-de-vale\\lo_de_vale_I4K_icon.ico")
app = Ventas(root)
app.mainloop()


# app.imprimir(fecha,hora,"1",ci,nomcliente,cifun,nomfuncio,lista)
