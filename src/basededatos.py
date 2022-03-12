import re
from tkinter import *
import mysql.connector

# aqui se pueden agregar datos a la base de datos


class Bd():
    # aqui se pueden buscar datos a la base de datos
    def __init__(self):
        self.miConexion = mysql.connector.connect(
            host='sql716.main-hosting.eu', user='u592463271_DiegoxD ', passwd='Diego123456', db='u592463271_Lodevale', port=3306)
        self.cur = self.miConexion.cursor()

    def iniciar(self):
        self.miConexion = mysql.connector.connect(
            host='sql716.main-hosting.eu', user='u592463271_DiegoxD ', passwd='Diego123456', db='u592463271_Lodevale', port=3306)
        self.cur = self.miConexion.cursor()

    def buscar(self):
        self.cur.execute("SELECT * FROM Producto")
        lista = self.cur.fetchall()
        return lista
    # consulta para eliminar productos

    def eliminar(self, codigo):
        sql = "DELETE FROM Producto WHERE codigo = %s;"
        self.cur.execute(sql, [codigo])
        self.miConexion.commit()

    def buscarnombre(self, codigo):
        sql = "SELECT * FROM Producto WHERE codigo = %s;"
        self.cur.execute(sql, [codigo])
        fila = self.cur.fetchone()
        return fila

    def insertar(self, pc, pv, nombre, cant, codigo):
        # print("insercion exitosa")
        sql1 = "INSERT INTO Producto (precioc, preciov,nombre,cantidad,codigo) VALUES (%s,%s,%s,%s,%s);"
        if self.buscarnombre(codigo) != None:
            vector = self.buscarnombre(codigo)
            suma = int(vector[4]) + int(cant)
            sql2 = "UPDATE Producto SET precioc = '{}', preciov = '{}', nombre = '{}', cantidad = '{}', codigo = '{}' WHERE codigo = '{}';".format(
                pc, pv, nombre, suma, codigo, codigo)
            self.cur.execute(sql2)
        else:
            self.cur.execute(sql1, [pc, pv, nombre, cant, codigo])
        self.miConexion.commit()

    def modificar(self, pc, pv, nombre, cant, codigo):
        # print("actualizacion exitosa")
        sql = "UPDATE Producto SET precioc = '{}', preciov = '{}', nombre = '{}', cantidad = '{}', codigo = '{}' WHERE codigo = '{}';".format(
            pc, pv, nombre, cant, codigo, codigo)
        self.cur.execute(sql)
        # print("actualizacion exitosa")
        self.miConexion.commit()

    def finalizar(self):
        # print("se guardo")
        self.miConexion.close()


#  aqui ira todo lo referente a ventas


    def insertarventa(self, fecha, total):
        print("venta insertada")
        sql1 = "INSERT INTO Ventas (fecha,total) VALUES (%s,%s);"
        self.cur.execute(sql1, [fecha, total])
        print("avanzo de venta")
        self.miConexion.commit()

    def insertardescripcion(self, idVenta, idProducto, cantidad):
        # print("descripcion insertada")
        sql1 = "INSERT INTO Descripcion (idVentas,idProducto,cant) VALUES (%s,%s,%s);"
        self.cur.execute(sql1, [idVenta, idProducto, cantidad])
        self.miConexion.commit()

    def buscarPorFecha(self, fecha):
        sql = "SELECT * FROM Ventas WHERE fecha = %s;"
        self.cur.execute(sql, [fecha])
        fila = self.cur.fetchall()
        return fila

    def buscarUltimaVenta(self):
        sql = "SELECT * FROM Ventas WHERE id IN (SELECT MAX(id) FROM Ventas);"
        self.cur.execute(sql)
        fila = self.cur.fetchone()
        return fila

    def buscarentrefechas(self, fecha1, fecha2):
        sql = "SELECT * FROM Ventas WHERE id BETWEEN %s AND %s;"
        self.cur.execute(sql, [fecha1, fecha2])
        fila = self.cur.fetchall()
        return fila

    def modificarporventa(self, id, cantidad):
        sql = "UPDATE Producto SET cantidad = '{}' WHERE id = '{}';".format(
            cantidad, id)
        self.cur.execute(sql)
        # print("actualizacion exitosa")
        self.miConexion.commit()
