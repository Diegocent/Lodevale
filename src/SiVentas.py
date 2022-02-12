from faulthandler import disable
from sre_parse import State
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from turtle import width
from click import command
import psycopg2
from tkinter import ttk

from declaracion import *


class Ventas(Frame):

    # # aqui se pueden buscar datos a la base de datos
    # def buscar(self):
    #     conn = psycopg2.connect(dbname="lodevale", user="postgres",
    #                             password="Diego123456", host="localhost", port="5432")
    #     cursor = conn.cursor()
    #     consulta = '''SELECT * FROM productos'''
    #     cursor.execute(consulta)

    #     fila = cursor.fetchall()
    #     # lista = Listbox(self.frame2, width=100, height=20,
    #     #                 font=("Arial", 18), fg="#707070")
    #     # lista.grid(row=10, columnspan=4, sticky=W+E)

    #     # for x in fila:
    #     #     lista.insert(END, x)
    #     #     lista.insert(END, "--------------------------------")

    #     conn.commit()
    #     conn.close()

    # # consulta para eliminar productos
    def eliminar():

        miConexion = mysql.connector.connect(
            host='localhost', user='USUARIO', passwd='PASS', db='neoguias')
        cur = miConexion.cursor()
        cur.execute("SELECT nombre, apellido FROM usuarios")
        for nombre, apellido in cur.fetchall():
            print(nombre, apellido)
        miConexion.close()

    # def eliminar(nombre):
    #     conn = psycopg2.connect(dbname="lodevale", user="postgres",
    #                             password="Diego123456", host="localhost", port="5432")
    #     cursor = conn.cursor()
    #     consulta = '''DELETE FROM productos WHERE nombre = %s; '''
    #     cursor.execute(consulta, [nombre])
    #     print('eliminado')
    #     conn.commit()
    #     conn.close()
    #     Ventas.buscar()

    # def buscarnombre(nombre):
    #     conn = psycopg2.connect(dbname="postgres", user="postgres",
    #                             password="Diego123456", host="localhost", port="5432")
    #     cursor = conn.cursor()
    #     consulta = '''SELECT * FROM productos WHERE nombre = %s'''
    #     cursor.execute(consulta, [nombre])

    #     fila = cursor.fetchone()
    #     print(fila)

    #     conn.commit()
    #     conn.close()
    #     Ventas.buscar()

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.resultado = DoubleVar()
        self.listap = []
        self.sumatotal = 0.0
        self.dato = " "
        self.ci = " "
        self.contador = 0
        self.efectivo = ""
        self.create_widfets()

    def Calculartotal(self, n1, n2):
        temp = int(n1)*int(n2)
        return temp

    def SumaLista(self, nombre, precio, cantidad, codigo):
        producto = TipoProducto(nombre, precio, cantidad, codigo)
        self.listap.append(producto)
        for x in self.listap:
            print(x.nombre)

    def CalculaPrecio(self, peso, tipo):
        print(peso)
        print(str(tipo))
        cal = float(peso)
        if tipo == 1:
            self.resultado = cal*25000
        elif tipo == 2:
            self.resultado = cal*30000
        elif tipo == 3:
            self.resultado = cal*35000
        elif tipo == 4:
            self.resultado = cal*80000
        # self.entry_codigo.delete(0, 'end')

    def cargarlista(self, codigo, cantidad, nombre, precio, subtotal):
        self.tv.insert("", END, text=codigo,
                       values=(nombre, cantidad, precio, subtotal))

        if codigo == "0":
            self.dato = self.entry_name.get()
            self.ci = self.entry_ci.get()
            self.SumaLista(nombre, subtotal, cantidad, codigo)
            self.sumatotal = self.sumatotal + float(subtotal)
            self.entry_total.config(state='normal')
            self.entry_total.delete(0, 'end')
            self.entry_total.insert(0, str(self.sumatotal))
            self.entry_total.config(state='disabled')
            self.entry_codigo.delete(0, 'end')
            self.entry_cantidad.delete(0, 'end')
        pass

    def Platos(self):
        print(self.entry_name.get())
        self.dato = self.entry_name.get()
        self.ci = self.entry_ci.get()

        self.ventanaplatos = TipoPlato(self.master)
        self.master.wait_window(self.ventanaplatos.nueva_ventana)
        self.CalculaPrecio(self.ventanaplatos.numero,
                           self.ventanaplatos.opcion.get())
        self.cargarlista(str(self.ventanaplatos.opcion.get()), str(self.ventanaplatos.numero),
                         self.ventanaplatos.nombre, self.ventanaplatos.precio, self.resultado)

        produc = TipoProducto(self.ventanaplatos.nombre, self.resultado,
                              self.ventanaplatos.numero, self.ventanaplatos.opcion.get())
        self.listap.append(produc)

        self.sumatotal = self.sumatotal + self.resultado
        self.entry_total.config(state='normal')
        self.entry_total.delete(0, 'end')
        self.entry_total.insert(0, str(self.sumatotal))
        self.entry_total.config(state='disabled')

        for x in self.listap:
            print(x.nombre)

    def Vueltos(self, fecha, hora, caja, ci, nomcliente, nomfuncio, cifun):
        self.ventanavuelto = Vuelto(self.sumatotal, self.master)
        self.master.wait_window(self.ventanavuelto.vuelto)
        self.contador = self.contador + 1
        self.efectivo = self.ventanavuelto.nuevo
        self.imprimir(fecha, hora, caja, ci, nomcliente,
                      nomfuncio, cifun, self.ventanavuelto.monto)

        messagebox.showinfo(message="Compra culminada",
                            title="Completado con exito")
        self.imprimir(fecha, hora, caja, ci, nomcliente,
                      nomfuncio, cifun, self.ventanavuelto.monto)

        self.tv.delete(*self.tv.get_children())
        self.listap.clear()
        self.sumatotal = 0
        self.entry_name.delete(0, 'end')
        self.entry_ci.delete(0, 'end')
        self.entry_total.config(state="normal")
        self.entry_total.delete(0, 'end')
        self.entry_total.config(state="disable")
        self.dato = " "

    # def pasar(self, cant):
    #     cantidad = cant
    #     self.entry_codigo.focus()

    def create_widfets(self):
        self.frame1 = Frame()
        self.frame1.place(relx=0.2, rely=0.0, relheight=0.33, relwidth=0.8)
        self.frame1.config(bg="#b4cbca")

        self.frame2 = Frame()
        self.frame2.place(relx=0.2, rely=0.33, relheight=0.5, relwidth=0.8)
        self.frame2.config(bg="#deecec")

        self.frame3 = Frame()
        self.frame3.place(relx=0.2, rely=0.83, relheight=0.17, relwidth=0.8)
        self.frame3.config(bg="#d5f4f4")

        self.frame4 = Frame()
        self.frame4.place(relx=0.0, rely=0.0, relheight=1, relwidth=0.2)
        self.frame4.config(bg="#1b4a4a")

        self.label1 = Label(self.frame1, text="Nueva venta",
                            font=("Arial", 18), fg="#707070", bg="#b4cbca")
        self.label1.grid(row=0, column=0)

        # aqui se recibe la fecha
        self.label2 = Label(self.frame1, text="Fecha",
                            anchor="w", bg="#b4cbca")
        self.label2.grid(padx=5, pady=5, row=1, column=0, sticky=E+W)

        self.entry_date = Entry(self.frame1)
        self.entry_date.grid(padx=5, pady=5, row=2,
                             column=0, sticky=E+W, ipady=5)
        now = datetime.now()
        self.entry_date.insert(0, now.strftime("%d/%m/%Y"))
        self.entry_date.config(state='disabled')

        # aqui se recibe el nombre del cliente
        self.label3 = Label(self.frame1, text="Señor:",
                            anchor="w", bg="#b4cbca")
        self.label3.grid(padx=5, pady=5, row=1, column=2, sticky=E+W)

        self.entry_name = Entry(self.frame1)
        self.entry_name.grid(padx=5, pady=5, row=2,
                             column=2, sticky=E+W, ipady=5)

        # aqui se recibe el ruc del cliente
        self.label4 = Label(self.frame1, text="C.I/RUC N:",
                            anchor="w", bg="#b4cbca")
        self.label4.grid(padx=5, pady=5, row=3, column=0, sticky=E+W)

        self.entry_ci = Entry(self.frame1)
        self.entry_ci.grid(padx=5, pady=5, row=4,
                           column=0, sticky=E+W, ipady=5)

        # se puede recibir la descripcion de la empresa que pueda tener
        self.label4 = Label(self.frame1, text="Descripcion:",
                            anchor="w", bg="#b4cbca")
        self.label4.grid(padx=5, pady=5, row=3, column=2, sticky=E+W)

        self.entry_descripcion = Entry(self.frame1)
        self.entry_descripcion.grid(
            padx=5, pady=5, row=4, column=2, sticky=E+W, ipady=5)
        # aqui se reciben la cantidad y el codigo del objeto

        self.entry_cantidad = Entry(self.frame1)
        self.entry_cantidad.grid(
            padx=10, pady=10, row=5, column=0, ipady=5, ipadx=1)
        self.entry_cantidad.focus()
        self.entry_cantidad.bind(
            '<Return>', lambda e: e.widget.tk_focusNext().focus_set())
        self.entry_codigo = Entry(self.frame1)
        self.entry_codigo.grid(padx=5, pady=5, row=5, column=1,
                               columnspan=4, sticky=E+W, ipady=5)
        self.entry_codigo.bind(
            '<Return>', lambda e: e.widget.tk_focusNext().focus_set())

        self.label6 = Label(self.frame1, text="Cantidad",
                            bg="#b4cbca", anchor=CENTER)
        self.label6.grid(row=6, column=0, sticky=E+W)
        self.label6 = Label(self.frame1, text="Codigo",
                            bg="#b4cbca", anchor=CENTER)
        self.label6.grid(row=6, column=1, sticky=E+W, columnspan=4)
        # codigo, cantidad, nombre, precio, subtotal)
        self.button = Button(self.frame1, fg="white", bg="#009E20",
                             text="Agregar Producto", width=20, command=lambda: self.cargarlista("0", self.entry_cantidad.get(), "Varios", self.entry_codigo.get(), self.Calculartotal(self.entry_codigo.get(), self.entry_cantidad.get())), cursor="hand2")
        self.button.grid(padx=5, pady=5, row=5, column=5,
                         sticky=W+E, columnspan=3)

        self.button2 = Button(self.frame1, fg="black", bg="#00EEFF",
                              text="Platos", width=20, command=lambda: self.Platos(), cursor="hand2")
        self.button2.grid(padx=5, pady=5, row=5, column=8,
                          columnspan=3, sticky=W+E)

        # en esta parte se controla la tabla
        self.scroll = Scrollbar(self.frame2)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.tv = ttk.Treeview(self.frame2, columns=(
            "Colum1", "Colum2", "Colum3", "Colum4"), yscrollcommand=self.scroll.set, selectmode="none")
        self.tv.pack(expand=True, fill=BOTH)
        self.scroll.config(command=self.tv.yview)
        self.tv.heading("#0", text="Codigo", anchor=CENTER)
        self.tv.heading("Colum1", text="Descripcion",
                        anchor=CENTER)
        self.tv.heading("Colum2", text="Cantidad",
                        anchor=CENTER)
        self.tv.heading("Colum3", text="Precio", anchor=CENTER)
        self.tv.heading("Colum4", text="Sub Total",
                        anchor=CENTER)

        # aqui se muestra el total
        self.Total = Label(self.frame3, text="Total",
                           bg="#BDEDBD", font=("Arial", 24))
        self.Total.grid(row=0, column=0, sticky=E+W,
                        columnspan=3, padx=2, pady=2, ipady=5)

        self.entry_total = Entry(self.frame3, font=("Arial", 24))
        self.entry_total.grid(padx=5, pady=5, row=0, column=3,
                              columnspan=2, sticky=E+W, ipady=5)
        self.entry_total.config(state="disable")

        # aqui se gestiona el menu de la izquierda
        self.file_image = PhotoImage(
            file="C:\\Users\\USER\\Desktop\\Lo-de-vale\\lo de vale.png")
        # self.file_imagezoon = self.file_image.subsample(3)
        self.imagen = Label(self.frame4, image=self.file_image)
        self.imagen.place(x=50, y=50, width=200, height=200)

        # apartado para la parte de impresion
        fecha = now.strftime("%d/%m/%Y")
        hora = now.strftime("%H:%M:%S")
        caja = "2"

        ci = self.entry_ci.get()
        nomcliente = self.entry_name.get()

        cajero = Cajero("Rocio", " ")
        nomfuncio = cajero.nombre
        cifun = cajero.ruc

        self.botonfinalizar = Button(self.frame3, fg="black", bg="#00EEFF",
                                     text="Finalizar", width=20, cursor="hand2", command=lambda: self.Vueltos(fecha, hora, caja, ci, nomcliente, cifun, nomfuncio))
        self.botonfinalizar.grid(padx=5, pady=5, row=0, column=8,
                                 columnspan=3, sticky=W+E)

    # def enviar(nombre, precio, cantidad):
    #     conn = psycopg2.connect(dbname="lodevale", user="postgres",
    #                             password="postgres", host="localhost", port="5432")
    #     cursor = conn.cursor()
    #     consulta = '''INSERT INTO productos(nombre, precio, cantidad) VALUES (%s,%s,%s)'''
    #     cursor.execute(consulta, (nombre, precio, cantidad))
    #     print('datos guardados')
    #     conn.commit()
    #     conn.close()
    #     Ventas.buscar()

    def imprimir(self, fecha, hora, caja, ci, nomcliente, cifun, nomfuncio, vuelto):

        impresion = open(r'\\localhost\\Miimpresora', 'w')
        impresion.write("       COMEDOR LO DE VALE       \n")
        impresion.write("AV.PITIANTUTA CASI PAZ DEL CHACO\n")
        impresion.write("================================\n")
        impresion.write("Fecha: "+fecha+" Hora: "+hora+"\n")
        impresion.write("Caja:   "+caja+"       \n")
        impresion.write("Cliente:  "+self.ci+" - "+self.dato+"\n")
        impresion.write("Vendedor: "+nomfuncio+"\n")
        impresion.write("\n")
        impresion.write("================================\n")
        impresion.write("Cant.   Producto     SubTotal \n")

        i = 0
        for x in self.listap:
            impresion.write(str(x.cantidad)+"    "+x.nombre+"   "+str(
                x.precio)+"\n")
            i = i+1
        impresion.write("================================\n")
        impresion.write("\n")
        impresion.write("Total:"+str(self.sumatotal)+" \n")
        impresion.write("Efectivo:"+str(self.efectivo)+" \n")
        impresion.write("Su vuelto es:"+str(vuelto)+"\n")
        impresion.write("================================\n")
        impresion.write(" Ticket N°.:"+str(self.contador) + " \n")
        impresion.write("================================\n")
        impresion.write(" *Muchas gracias por su compra* \n")

        impresion.close()


class TipoPlato(Frame):
    def __init__(self, master=None):
        super().__init__(master, width=320, height=220)
        self.master = master
        self.nueva_ventana = Toplevel()
        self.nueva_ventana.title("Kilaje de comida")
        self.nueva_ventana.geometry("350x220")
        self.opcion = IntVar()
        self.numero = DoubleVar()
        self.nombre = ""
        self.precio = ""
        self.Mostrar()

    def guardar(self, num, opcion1):
        self.numero = num
        # print(self.numero)
        if opcion1 == 1:
            self.nombre = "Plato Normal"
            self.precio = "25.000"
        elif opcion1 == 2:
            self.nombre = "Especial"
            self.precio = "30.000"
        elif opcion1 == 3:
            self.nombre = "Milanesas"
            self.precio = "35.000"
        elif opcion1 == 4:
            self.nombre = "Plato de Asado"
            self.precio = "80.000"
        # print(self.nombre)
        self.nueva_ventana.destroy()

    def Mostrar(self):

        # Como StrinVar pero en entero

        r1 = Radiobutton(self.nueva_ventana, text="Normal",
                         value=1, variable=self.opcion, anchor="w")
        r1.grid(row=1, column=1, sticky=E+W)
        r2 = Radiobutton(self.nueva_ventana, text="Especial",
                         value=2, variable=self.opcion, anchor="w")
        r2.grid(row=2, column=1, sticky=E+W)
        r3 = Radiobutton(self.nueva_ventana, text="Milanesas",
                         value=3, variable=self.opcion, anchor="w")
        r3.grid(row=3, column=1, sticky=E+W)
        r4 = Radiobutton(self.nueva_ventana, text="Asado",
                         value=4, variable=self.opcion, anchor="w")
        r4.grid(row=4, column=1, sticky=E+W)
        self.k = Label(self.nueva_ventana,
                       text="Ingrese el kilaje de la comida", anchor="w")
        self.k.grid(padx=5, pady=5, row=5, column=1, columnspan=2, sticky=E+W)

        self.entry_kilo = Entry(self.nueva_ventana)
        self.entry_kilo.grid(padx=5, pady=5, row=6, column=1,
                             columnspan=2, sticky=E+W)

        self.button2 = Button(self.nueva_ventana, fg="black", bg="#00EEFF",
                              text="OK", width=20, command=lambda: self.guardar(self.entry_kilo.get(), self.opcion.get()), cursor="hand2")
        self.button2.grid(padx=5, pady=5, row=7, column=1,
                          columnspan=3, sticky=W+E)
        # self.numero = int(self.entry_kilo)


class Vuelto(Frame):
    def __init__(self, came, master=None):
        super().__init__(master, width=320, height=220)
        self.master = master
        self.vuelto = Toplevel()
        self.vuelto.title("Calculo de vuelto")
        self.vuelto.geometry("350x220")
        self.monto = 0
        self.cambio = came
        self.nuevo = " "
        self.Mostrar()

    def calcular(self):
        aux = int(self.entry_monto.get())
        self.monto = aux - self.cambio

        self.entry_resultado.config(state='normal')
        self.entry_resultado.delete(0, 'end')
        self.entry_resultado.insert(0, str(self.monto))
        self.entry_resultado.config(state='disabled')

    def guardar(self, nu):
        self.nuevo = nu
        self.vuelto.destroy()

    def Mostrar(self):

        self.k = Label(self.vuelto,
                       text="Ingrese el Monto recibido")
        self.k.pack()

        self.entry_monto = Entry(self.vuelto)
        self.entry_monto.pack()

        self.l = Label(self.vuelto,
                       text="Total a pagar")
        self.l.pack()

        self.entry_cambio = Entry(self.vuelto)
        self.entry_cambio.pack()

        self.entry_cambio.config(state='normal')
        self.entry_cambio.delete(0, 'end')
        self.entry_cambio.insert(0, str(self.cambio))
        self.entry_cambio.config(state='disabled')

        self.m = Label(self.vuelto,
                       text="Total de vuelto")
        self.m.pack()

        self.entry_resultado = Entry(self.vuelto)
        self.entry_resultado.pack()
        self.entry_resultado.config(state='disabled')

        self.button1 = Button(self.vuelto, fg="black", bg="#00EEFF",
                              text="Calcular", width=20, command=lambda: self.calcular(), cursor="hand2")
        self.button1.pack()

        self.button2 = Button(self.vuelto, fg="black", bg="#00EEFF",
                              text="OK", width=20, command=lambda: self.guardar(self.entry_monto.get()), cursor="hand2")
        self.button2.pack()
