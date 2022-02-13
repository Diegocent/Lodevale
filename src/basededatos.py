import re
from tkinter import *
import mysql.connector

# aqui se pueden agregar datos a la base de datos


class Bd():
    # aqui se pueden buscar datos a la base de datos
    def buscar(self):
        miConexion = mysql.connector.connect(
            host='sql716.main-hosting.eu', user='u592463271_DiegoxD ', passwd='Diego123456', db='u592463271_Lodevale', port=3306)
        cur = miConexion.cursor()
        cur.execute("SELECT * FROM Producto")
        lista = cur.fetchall()
        print(lista)
        miConexion.close()
    # consulta para eliminar productos

    def eliminar(self, codigo):
        miConexion = mysql.connector.connect(
            host='sql716.main-hosting.eu', user='u592463271_DiegoxD ', passwd='Diego123456', db='u592463271_Lodevale', port=3306)
        cur = miConexion.cursor()
        sql = "DELETE FROM Producto WHERE codigo = %s;"
        cur.execute(sql, [codigo])
        miConexion.commit()
        miConexion.close()

    def buscarnombre(self, codigo):
        miConexion = mysql.connector.connect(
            host='sql716.main-hosting.eu', user='u592463271_DiegoxD ', passwd='Diego123456', db='u592463271_Lodevale', port=3306)
        cur = miConexion.cursor()
        sql = "SELECT * FROM Producto WHERE codigo = %s;"
        cur.execute(sql, [codigo])
        fila = cur.fetchone()
        print(fila)
        miConexion.close()
        return fila

    def insertar(self, pc, pv, nombre, cant, codigo):
        miConexion = mysql.connector.connect(
            host='sql716.main-hosting.eu', user='u592463271_DiegoxD ', passwd='Diego123456', db='u592463271_Lodevale', port=3306)
        cur = miConexion.cursor()
        print("insercion exitosa")
        sql = "INSERT INTO Producto (precioc, preciov,nombre,cantidad,codigo) VALUES (%s,%s,%s,%s,%s);"
        cur.execute(sql, (pc, pv, nombre, cant, codigo))
        miConexion.commit()
        miConexion.close()
