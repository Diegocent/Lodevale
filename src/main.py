from tkinter import *

from numpy import pad
from SiVentas import *
from declaracion import *
from datetime import datetime
import mysql.connector
from tkinter import ttk
from tkinter import messagebox


def establecerusuario(dato, clave):
    miConexion = mysql.connector.connect(
        host='sql716.main-hosting.eu', user='u592463271_DiegoxD ', passwd='Diego123456', db='u592463271_Lodevale', port=3306)
    cur = miConexion.cursor()
    sql = "SELECT * FROM Usuario WHERE nombre = %s;"
    cur.execute(sql, [dato])
    global fila
    fila = cur.fetchone()
    # print(fila)
    # print(dato)
    if fila[2] == clave:
        sql2 = "SELECT restante FROM CierreCaja WHERE id = %s;"
        sql3 = "SELECT a.caja, b.id FROM CierreCaja b INNER JOIN Usuario a ON b.idCajero= a.cod"

        cur.execute(sql3)
        aux2 = cur.fetchall()
        i = -1
        print(fila[4])
        print(aux2)
        while fila[4] != aux2[i][0]:
            i -= 1
        cur.execute(sql2, [aux2[i][1]])
        aux = cur.fetchone()
        print(aux)
        temp = aux[0]
        print(temp)
        global cierre
        cierre = float(temp)
        login.destroy()
    else:
        messagebox.showerror(message="Contraseña incorrecta",
                             title="Error al ingresar la clave")
    miConexion.close()


def veranterior(self, row):
    miConexion = mysql.connector.connect(
        host='sql716.main-hosting.eu', user='u592463271_DiegoxD ', passwd='Diego123456', db='u592463271_Lodevale', port=3306)
    cur = miConexion.cursor()
    sql = "SELECT * FROM Ventas WHERE id IN (SELECT MAX(id) FROM Ventas);"
    cur.execute(sql, [row])
    global cierre
    pass


def enviar(event):
    establecerusuario(entry_usuario.get(), entry_clave.get())


# nombre = input()
# cedula = input()
# direccion = input()
# cliente = Cliente(nombre,cedula, direccion)
# ci=cliente.ruc
# nomcliente=cliente.nombre
login = Tk()
login.geometry("400x200+500+200")
login.title("Inicio de sesion")
# login.overrideredirect(True)

Label(login, text="Ingrese su usuario", font=("Arial", 16)).pack()
entry_usuario = Entry(login)
entry_usuario.pack(ipadx=20, ipady=5)
entry_usuario.focus()
entry_usuario.bind('<Return>', lambda e: e.widget.tk_focusNext().focus_set())
Label(login, text="Contraseña", font=("Arial", 16)).pack()
entry_clave = Entry(login, show='*')
entry_clave.pack(ipadx=20, ipady=5)
entry_clave.bind('<Return>', lambda e: e.widget.tk_focusNext().focus_set())
boton = Button(login, text="INICIAR", command=lambda: establecerusuario(
    entry_usuario.get(), entry_clave.get()), bg='red', fg='#ffffff')
boton.pack(ipadx=20, ipady=5, padx=5, pady=5)
boton.bind('<Return>', enviar)

login.mainloop()

root = Tk()
root.title("En lo de Vale sistem")
root.geometry("1500x800+0+0")
# root.iconbitmap(
#     "C:\\Users\\USER\\Desktop\\Lo-de-vale\\lo_de_vale_I4K_icon.ico")
app = Ventas(fila, cierre, root)
app.mainloop()

# app.imprimir(fecha,hora,"1",ci,nomcliente,cifun,nomfuncio,lista)
