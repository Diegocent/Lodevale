import re
from tkinter import *
import psycopg2
root = Tk()
root.title("Lo de Vale")

# aqui se pueden agregar datos a la base de datos


class Bd:
    # aqui se pueden buscar datos a la base de datos
    def buscar(self):
        conn = psycopg2.connect(dbname="lodevale", user="postgres",
                                password="postgres", host="localhost", port="5432")
        cursor = conn.cursor()
        consulta = '''SELECT * FROM productos'''
        cursor.execute(consulta)

        fila = cursor.fetchall()
        lista = Listbox(self.frame2, width=20, height=10)
        lista.grid(row=10, columnspan=4, sticky=W+E)

        for x in fila:
            lista.insert(END, x)

        conn.commit()
        conn.close()

    def enviar(nombre, precio, cantidad):
        conn = psycopg2.connect(dbname="lodevale", user="postgres",
                                password="postgres", host="localhost", port="5432")
        cursor = conn.cursor()
        consulta = '''INSERT INTO productos(nombre, precio, cantidad) VALUES (%s,%s,%s)'''
        cursor.execute(consulta, (nombre, precio, cantidad))
        print('datos guardados')
        conn.commit()
        conn.close()
        buscar()

    # consulta para eliminar productos

    def eliminar(nombre):
        conn = psycopg2.connect(dbname="lodevale", user="postgres",
                                password="postgres", host="localhost", port="5432")
        cursor = conn.cursor()
        consulta = '''DELETE FROM productos WHERE nombre = %s; '''
        cursor.execute(consulta, [nombre])
        print('eliminado')
        conn.commit()
        conn.close()
        buscar()

    def buscarnombre(nombre):
        conn = psycopg2.connect(dbname="postgres", user="postgres",
                                password="Diego123456", host="localhost", port="5432")
        cursor = conn.cursor()
        consulta = '''SELECT * FROM productos WHERE nombre = %s'''
        cursor.execute(consulta, [nombre])

        fila = cursor.fetchone()
        print(fila)

        conn.commit()
        conn.close()
        buscar()

    # # canvas donde se agregan los imputs
    # canvas = Canvas(root, height=380, width=400)
    # canvas.pack()

    # frame1 = Frame()
    # frame1.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)

    # label = Label(frame1, text="Agregar producto")
    # label.grid(row=0, column=1)

    # # aqui se recibe el nombre
    # label = Label(frame1, text="Nombre")
    # label.grid(row=1, column=0)

    # entry_name = Entry(frame1)
    # entry_name.grid(row=1, column=1)

    # # aqui se recibe el precio
    # label = Label(frame1, text="precio")
    # label.grid(row=2, column=0)

    # entry_precio = Entry(frame1)
    # entry_precio.grid(row=2, column=1)

    # # aqui se recibe la cantidad
    # label = Label(frame1, text="cantidad")
    # label.grid(row=3, column=0)

    # entry_cantidad = Entry(frame1)
    # entry_cantidad.grid(row=3, column=1)

    # button = Button(frame1, fg="white", bg="blue", text="enviar", command=lambda: enviar(
    #     entry_name.get(),
    #     entry_precio.get(),
    #     entry_cantidad.get()
    # ))
    # button.grid(row=4, column=1, sticky=W+E)

    # buscar()

    # button2 = Button(frame1, text="eliminar",
    #                  command=lambda: eliminar(entry_name.get()))
    # button2.grid(row=5, column=1, sticky=W+E)

    # # buscar
    # label = Label(frame1, text="buscar datos")
    # label.grid(row=6, column=1)

    # label = Label(frame1, text="buscar por numero")
    # label.grid(row=7, column=0)

    # entry_buscar = Entry(frame1)
    # entry_buscar.grid(row=7, column=1)
    # button3 = Button(frame1, text="buscar",
    #                  command=lambda: buscarnombre(entry_buscar.get()))
    # button3.grid(row=7, column=2, sticky=W+E)

    # root.mainloop()
