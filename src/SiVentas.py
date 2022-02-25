from faulthandler import disable
from multiprocessing import connection
from sqlite3 import connect
from sre_parse import State
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from turtle import bgcolor, width
from click import command
import mysql.connector
from tkinter import ttk
from basededatos import *
from declaracion import *


class Ventas(Frame):

    def __init__(self, nombre, caja, ci, master=None):
        super().__init__(master)
        self.master = master
        self.resultado = DoubleVar()
        self.listap = []
        self.sumatotal = 0.0
        self.dato = " "
        self.ci = " "
        self.contador = 0
        self.efectivo = ""
        self.db = Bd()
        self.nomfuncio = nombre
        self.caja = caja
        self.cifun = ci
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
        self.entry_cantidad.delete(0, 'end')
        self.entry_codigo.delete(0, 'end')
        self.entry_cantidad.focus()

    def buscardatos(self, cantidad, codigo):
        dato = self.db.buscarnombre(codigo)
        print(dato)
        cod = dato[5]
        cant = cantidad
        nombre = dato[3]
        precio = dato[2]
        total = self.Calculartotal(cantidad, precio)
        self.cargarlista(cod, cant, nombre, precio, total)

        self.sumatotal = self.sumatotal + float(total)
        self.entry_total.config(state='normal')
        self.entry_total.delete(0, 'end')
        self.entry_total.insert(0, str(self.sumatotal))
        self.entry_total.config(state='disabled')
        self.entry_cantidad.delete(0, 'end')
        self.entry_codigo.delete(0, 'end')
        self.entry_cantidad.focus()

    def agregarproducto(self, event):
        self.buscardatos(self.entry_cantidad.get(), self.entry_codigo.get())
        pass
    # aqui se manda a la ventana de agregar producto

    def administrarproductos(self):
        self.productos = Producto(self.master)
        self.master.wait_window(self.productos.producto)
    # aqui se manda a la ventana de modificar productos

    def modificarproductos(self):
        self.modproduc = Modulo(self.master)
        self.master.wait_window(self.modproduc.modulo)
    # aqui se manda a la ventana de eliminar productos

    def eliminarproductos(self):
        self.eliminar = Eliminacion(self.master)
        self.master.wait_window(self.eliminar.eliminar)

    def cliente(self, event):
        miConexion = mysql.connector.connect(
            host='sql716.main-hosting.eu', user='u592463271_DiegoxD ', passwd='Diego123456', db='u592463271_Lodevale', port=3306)
        cur = miConexion.cursor()
        sql = "SELECT * FROM Cliente WHERE ci = %s;"
        cur.execute(sql, [self.entry_ci.get()])
        fila = cur.fetchone()
        self.entry_name.insert(0, fila[1])
        print(fila)
        miConexion.close()

    # aqui se genera la pantalla principal
    def create_widfets(self):

        print(self.nomfuncio + ' ' + self.cifun + ' ' + self.caja)
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
        self.entry_ci.bind('<Return>', self.cliente)

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
        self.button1 = Button(self.frame1, fg="white", bg="#009E20",
                              text="Agregar Producto", width=20, command=lambda: self.buscardatos(self.entry_cantidad.get(), self.entry_codigo.get()), cursor="hand2")
        self.button1.grid(padx=5, pady=5, row=5, column=5,
                          sticky=W+E, columnspan=3)
        self.button1.bind(
            '<Return>', self.agregarproducto)

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
            file="C:\\Users\\USER\\Desktop\\Lo-de-vale\\lodevale.png")
        # self.file_imagezoon = self.file_image.subsample(3)
        self.imagen = Label(self.frame4, image=self.file_image)
        self.imagen.place(x=50, y=50, width=200, height=200)

        self.botonproductos = Button(self.frame4, fg="black", bg="#00EEFF",
                                     text="Agregar compras", width=20, cursor="hand2", command=lambda: self.administrarproductos())
        self.botonproductos.place(x=50, y=280, width=200, height=50)

        self.botonproductos = Button(self.frame4, fg="black", bg="#00EEFF",
                                     text="Modificar Productos", width=20, cursor="hand2", command=lambda: self.modificarproductos())
        self.botonproductos.place(x=50, y=340, width=200, height=50)

        self.botonproductos = Button(self.frame4, fg="black", bg="#00EEFF",
                                     text="Eliminar productos", width=20, cursor="hand2", command=lambda: self.eliminarproductos())
        self.botonproductos.place(x=50, y=400, width=200, height=50)

        # apartado para la parte de impresion
        fecha = now.strftime("%d/%m/%Y")
        hora = now.strftime("%H:%M:%S")

        ci = self.entry_ci.get()
        nomcliente = self.entry_name.get()

        self.botonfinalizar = Button(self.frame3, fg="black", bg="#00EEFF",
                                     text="Finalizar", width=20, cursor="hand2", command=lambda: self.Vueltos(fecha, hora, self.caja, ci, nomcliente, self.cifun, self.nomfuncio))
        self.botonfinalizar.grid(padx=5, pady=5, row=0, column=8,
                                 columnspan=3, sticky=W+E)

    # aqui se imprime en la impresora de ticket
    def imprimir(self, fecha, hora, caja, ci, nomcliente, cifun, nomfuncio, vuelto):

        impresion = open(r'\\localhost\\Miimpresora', 'w')
        impresion.write("       COMEDOR LO DE VALE       \n")
        impresion.write("AV.PITIANTUTA CASI PAZ DEL CHACO\n")
        impresion.write("================================\n")
        impresion.write("Fecha: "+fecha+" Hora: "+hora+"\n")
        impresion.write("Caja:   "+self.caja+"       \n")
        impresion.write("Cliente:  "+self.ci+" - "+self.dato+"\n")
        impresion.write("Vendedor: "+self.nomfuncio+"\n")
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

# aqui se muestra la pantalla de peso del plato


class TipoPlato(Frame):
    def __init__(self, master=None):
        super().__init__(master, width=320, height=220)
        self.master = master
        self.nueva_ventana = Toplevel()
        self.nueva_ventana.title("Kilaje de comida")
        self.nueva_ventana.geometry("350x220+500+200")
        # esto oculta la parte del titulo
        self.nueva_ventana.overrideredirect(True)
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

    def mandar(self, event):
        self.guardar(self.entry_kilo.get(), self.opcion.get())

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
        self.entry_kilo.focus()
        self.entry_kilo.bind('<Return>', self.mandar)

        self.button2 = Button(self.nueva_ventana, fg="black", bg="#00EEFF",
                              text="OK", width=20, command=lambda: self.guardar(self.entry_kilo.get(), self.opcion.get()), cursor="hand2")
        self.button2.grid(padx=5, pady=5, row=7, column=1,
                          columnspan=3, sticky=W+E)
        # self.numero = int(self.entry_kilo)

# aqui se muestra la pantalla vuelto


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

    def enviarguardar(self, event):
        self.guardar(self.entry_monto.get())

    def vervuelto(self, event):
        self.calcular()
        self.button2.focus()

    def Mostrar(self):

        self.k = Label(self.vuelto,
                       text="Ingrese el Monto recibido")
        self.k.pack()

        self.entry_monto = Entry(self.vuelto)
        self.entry_monto.pack()
        self.entry_monto.focus()
        self.entry_monto.bind('<Return>', self.vervuelto)

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
        self.button2.bind('<Return>', self.enviarguardar)

# aqui se agregan los productos


class Producto(Frame):
    def __init__(self, master=None):
        super().__init__(master, width=320, height=220)
        self.master = master
        self.producto = Toplevel()
        self.producto.title("Agregar productos")
        self.producto.geometry("1060x720+50+50")
        self.db = Bd()
        self.Mostrar()

    def cargarlista(self, codigo, nombre, precioc, preciov, cantidad):
        self.tv.insert("", END, text=codigo,
                       values=(nombre, precioc, preciov, cantidad))

    def mostrartabla(self):
        dato = self.db.buscar()
        for x in dato:
            self.cargarlista(x[5], x[3], x[1], x[2], x[4])
            print(x)

    def guardardatos(self):
        self.db.insertar(self.entry_pc.get(), self.entry_pv.get(),
                         self.entry_np.get(), self.entry_cant.get(), self.entry_barras.get())
        self.entry_barras.delete(0, 'end')
        self.entry_cant.delete(0, 'end')
        self.entry_np.delete(0, 'end')
        self.entry_pc.delete(0, 'end')
        self.entry_pv.delete(0, 'end')
        self.entry_barras.focus()
        self.tv.delete(*self.tv.get_children())
        self.mostrartabla()

    def cargar(self, event):
        self.guardardatos()

    def guardar(self):
        self.producto.destroy()

    def Mostrar(self):

        self.frame1 = Frame(self.producto)
        self.frame1.place(relx=0, rely=0.0, relheight=0.33, relwidth=1)
        self.frame1.config(bg="#b4cbca")

        self.frame2 = LabelFrame(self.producto)
        self.frame2.place(relx=0, rely=0.33, relheight=0.5, relwidth=1)
        self.frame2.config(bg="#deecec")

        self.frame3 = Frame(self.producto)
        self.frame3.place(relx=0, rely=0.83, relheight=0.17, relwidth=1)
        self.frame3.config(bg="#d5f4f4")

        self.label1 = Label(self.frame1, text="Nuevo Producto",
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

        # aqui se recibe el codigo de barras del producto
        self.label3 = Label(self.frame1, text="Codigo de barras",
                            anchor="w", bg="#b4cbca")
        self.label3.grid(padx=5, pady=5, row=1, column=1, sticky=E+W)

        self.entry_barras = Entry(self.frame1)
        self.entry_barras.grid(padx=5, pady=5, row=2,
                               column=1, sticky=E+W, ipady=5)
        self.entry_barras.focus()
        self.entry_barras.bind(
            '<Return>', lambda e: e.widget.tk_focusNext().focus_set())

        # aqui se recibe el nombre del producto
        self.label4 = Label(self.frame1, text="Nombre del producto",
                            anchor="w", bg="#b4cbca")
        self.label4.grid(padx=5, pady=5, row=1, column=2, sticky=E+W)

        self.entry_np = Entry(self.frame1)
        self.entry_np.grid(padx=5, pady=5, row=2,
                           column=2, sticky=E+W, ipady=5)
        self.entry_np.bind(
            '<Return>', lambda e: e.widget.tk_focusNext().focus_set())

        # se puede recibir precio de compra
        self.label4 = Label(self.frame1, text="Precio de compra",
                            anchor="w", bg="#b4cbca")
        self.label4.grid(padx=5, pady=5, row=3, column=0, sticky=E+W)

        self.entry_pc = Entry(self.frame1)
        self.entry_pc.grid(
            padx=5, pady=5, row=4, column=0, sticky=E+W, ipady=5)
        self.entry_pc.bind(
            '<Return>', lambda e: e.widget.tk_focusNext().focus_set())

        # se puede recibir precio de venta
        self.label4 = Label(self.frame1, text="Precio de Venta",
                            anchor="w", bg="#b4cbca")
        self.label4.grid(padx=5, pady=5, row=3, column=1, sticky=E+W)

        self.entry_pv = Entry(self.frame1)
        self.entry_pv.grid(
            padx=5, pady=5, row=4, column=1, sticky=E+W, ipady=5)
        self.entry_pv.bind(
            '<Return>', lambda e: e.widget.tk_focusNext().focus_set())

        # se puede recibir la cantidad
        self.label4 = Label(self.frame1, text="Cantidad",
                            anchor="w", bg="#b4cbca")
        self.label4.grid(padx=5, pady=5, row=3, column=2, sticky=E+W)

        self.entry_cant = Entry(self.frame1)
        self.entry_cant.grid(
            padx=5, pady=5, row=4, column=2, sticky=E+W, ipady=5)
        self.entry_cant.bind(
            '<Return>', lambda e: e.widget.tk_focusNext().focus_set())

        self.button1 = Button(self.frame1, fg="white", bg="#009E20",
                              text="Agregar Producto", width=20, command=lambda: self.guardardatos(), cursor="hand2")
        self.button1.grid(padx=5, pady=5, row=5, column=5,
                          sticky=W+E, columnspan=3)
        self.button1.bind('<Return>', self.cargar)

        # en esta parte se controla la tabla
        self.scroll = Scrollbar(self.frame2)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.tv = ttk.Treeview(self.frame2, columns=(
            "Colum1", "Colum2", "Colum3", "Colum4"), yscrollcommand=self.scroll.set, selectmode="none")
        self.tv.pack(expand=True, fill=BOTH)
        self.scroll.config(command=self.tv.yview)
        self.tv.heading("#0", text="Codigo de barras", anchor=CENTER)
        self.tv.heading("Colum1", text="Nombre",
                        anchor=CENTER)
        self.tv.heading("Colum2", text="Precio de Compra",
                        anchor=CENTER)
        self.tv.heading("Colum3", text="Precio de Venta", anchor=CENTER)
        self.tv.heading("Colum4", text="Cantidad",
                        anchor=CENTER)
        self.mostrartabla()

        # aqui se muestra el total
        # self.Total = Label(self.frame3, text="Total",
        #                    bg="#BDEDBD", font=("Arial", 24))
        # self.Total.grid(row=0, column=0, sticky=E+W,
        #                 columnspan=3, padx=2, pady=2, ipady=5)

        # self.entry_total = Entry(self.frame3, font=("Arial", 24))
        # self.entry_total.grid(padx=5, pady=5, row=0, column=3,
        #                       columnspan=2, sticky=E+W, ipady=5)
        # self.entry_total.config(state="disable")
        self.finalizar = Button(self.frame3, fg="white", bg="#009E20",
                                text="Finalizar", width=20, command=lambda: self.guardar(), cursor="hand2")
        self.finalizar.place(relx=0.2, rely=0.2, relheight=0.5, relwidth=0.5)

# aqui se modifican los productos


class Modulo(Frame):
    def __init__(self, master=None):
        super().__init__(master, width=320, height=220)
        self.master = master
        self.modulo = Toplevel()
        self.modulo.title("Modificar productos")
        self.modulo.geometry("1060x720+50+50")
        self.db = Bd()
        self.Mostrar()

    def cargarlista(self, codigo, nombre, precioc, preciov, cantidad):
        self.tv.insert("", END, text=codigo,
                       values=(nombre, precioc, preciov, cantidad))

    def mostrartabla(self):
        dato = self.db.buscar()
        for x in dato:
            self.cargarlista(x[5], x[3], x[1], x[2], x[4])

    def guardardatos(self):
        self.db.modificar(self.entry_pc.get(), self.entry_pv.get(),
                          self.entry_np.get(), self.entry_cant.get(), self.entry_barras.get())
        self.entry_barras.delete(0, 'end')
        self.entry_cant.delete(0, 'end')
        self.entry_np.delete(0, 'end')
        self.entry_pc.delete(0, 'end')
        self.entry_pv.delete(0, 'end')
        self.entry_barras.focus()
        self.tv.delete(*self.tv.get_children())
        self.mostrartabla()

    def cargar(self, event):
        self.guardardatos()

    def guardar(self):
        self.modulo.destroy()

    def cargardatos(self, event):
        self.entry_np.focus()

        temp = self.db.buscarnombre(self.entry_barras.get())
        self.entry_np.insert(0, temp[3])
        self.entry_pc.insert(0, temp[1])
        self.entry_pv.insert(0, temp[2])
        self.entry_cant.insert(0, temp[4])

    def Mostrar(self):

        self.frame1 = Frame(self.modulo)
        self.frame1.place(relx=0, rely=0.0, relheight=0.33, relwidth=1)
        self.frame1.config(bg="#b4cbca")

        self.frame2 = LabelFrame(self.modulo)
        self.frame2.place(relx=0, rely=0.33, relheight=0.5, relwidth=1)
        self.frame2.config(bg="#deecec")

        self.frame3 = Frame(self.modulo)
        self.frame3.place(relx=0, rely=0.83, relheight=0.17, relwidth=1)
        self.frame3.config(bg="#d5f4f4")

        self.label1 = Label(self.frame1, text="Modificar Producto",
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

        # aqui se recibe el codigo de barras del producto
        self.label3 = Label(self.frame1, text="Codigo de barras",
                            anchor="w", bg="#b4cbca")
        self.label3.grid(padx=5, pady=5, row=1, column=1, sticky=E+W)

        self.entry_barras = Entry(self.frame1)
        self.entry_barras.grid(padx=5, pady=5, row=2,
                               column=1, sticky=E+W, ipady=5)
        self.entry_barras.focus()
        self.entry_barras.bind(
            '<Return>', self.cargardatos)

        # aqui se recibe el nombre del producto
        self.label4 = Label(self.frame1, text="Nombre del producto",
                            anchor="w", bg="#b4cbca")
        self.label4.grid(padx=5, pady=5, row=1, column=2, sticky=E+W)

        self.entry_np = Entry(self.frame1)
        self.entry_np.grid(padx=5, pady=5, row=2,
                           column=2, sticky=E+W, ipady=5)
        self.entry_np.bind(
            '<Return>', lambda e: e.widget.tk_focusNext().focus_set())

        # se puede recibir precio de compra
        self.label4 = Label(self.frame1, text="Precio de compra",
                            anchor="w", bg="#b4cbca")
        self.label4.grid(padx=5, pady=5, row=3, column=0, sticky=E+W)

        self.entry_pc = Entry(self.frame1)
        self.entry_pc.grid(
            padx=5, pady=5, row=4, column=0, sticky=E+W, ipady=5)
        self.entry_pc.bind(
            '<Return>', lambda e: e.widget.tk_focusNext().focus_set())

        # se puede recibir precio de venta
        self.label4 = Label(self.frame1, text="Precio de Venta",
                            anchor="w", bg="#b4cbca")
        self.label4.grid(padx=5, pady=5, row=3, column=1, sticky=E+W)

        self.entry_pv = Entry(self.frame1)
        self.entry_pv.grid(
            padx=5, pady=5, row=4, column=1, sticky=E+W, ipady=5)
        self.entry_pv.bind(
            '<Return>', lambda e: e.widget.tk_focusNext().focus_set())

        # se puede recibir la cantidad
        self.label4 = Label(self.frame1, text="Cantidad",
                            anchor="w", bg="#b4cbca")
        self.label4.grid(padx=5, pady=5, row=3, column=2, sticky=E+W)

        self.entry_cant = Entry(self.frame1)
        self.entry_cant.grid(
            padx=5, pady=5, row=4, column=2, sticky=E+W, ipady=5)
        self.entry_cant.bind(
            '<Return>', lambda e: e.widget.tk_focusNext().focus_set())

        self.button1 = Button(self.frame1, fg="white", bg="#009E20",
                              text="Modificar Producto", width=20, command=lambda: self.guardardatos(), cursor="hand2")
        self.button1.grid(padx=5, pady=5, row=5, column=5,
                          sticky=W+E, columnspan=3)
        self.button1.bind('<Return>', self.cargar)

        # en esta parte se controla la tabla
        self.scroll = Scrollbar(self.frame2)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.tv = ttk.Treeview(self.frame2, columns=(
            "Colum1", "Colum2", "Colum3", "Colum4"), yscrollcommand=self.scroll.set, selectmode="none")
        self.tv.pack(expand=True, fill=BOTH)
        self.scroll.config(command=self.tv.yview)
        self.tv.heading("#0", text="Codigo de barras", anchor=CENTER)
        self.tv.heading("Colum1", text="Nombre",
                        anchor=CENTER)
        self.tv.heading("Colum2", text="Precio de Compra",
                        anchor=CENTER)
        self.tv.heading("Colum3", text="Precio de Venta", anchor=CENTER)
        self.tv.heading("Colum4", text="Cantidad",
                        anchor=CENTER)
        self.mostrartabla()
        # aqui se muestra el total
        # self.Total = Label(self.frame3, text="Total",
        #                    bg="#BDEDBD", font=("Arial", 24))
        # self.Total.grid(row=0, column=0, sticky=E+W,
        #                 columnspan=3, padx=2, pady=2, ipady=5)

        # self.entry_total = Entry(self.frame3, font=("Arial", 24))
        # self.entry_total.grid(padx=5, pady=5, row=0, column=3,
        #                       columnspan=2, sticky=E+W, ipady=5)
        # self.entry_total.config(state="disable")
        self.finalizar = Button(self.frame3, fg="white", bg="#009E20",
                                text="Finalizar", width=20, command=lambda: self.guardar(), cursor="hand2")
        self.finalizar.place(relx=0.2, rely=0.2, relheight=0.5, relwidth=0.5)


class Eliminacion(Frame):
    def __init__(self, master=None):
        super().__init__(master, width=320, height=220)
        self.master = master
        self.eliminar = Toplevel()
        self.eliminar.title("Eliminar productos")
        self.eliminar.geometry("1060x720+50+50")
        self.db = Bd()
        self.Mostrar()

    def cargarlista(self, codigo, nombre, precioc, preciov, cantidad):
        self.tv.insert("", END, text=codigo,
                       values=(nombre, precioc, preciov, cantidad))

    def mostrartabla(self):
        dato = self.db.buscar()
        for x in dato:
            self.cargarlista(x[5], x[3], x[1], x[2], x[4])

    def guardardatos(self):
        self.db.eliminar(self.entry_barras.get())
        self.entry_barras.delete(0, 'end')
        self.entry_barras.focus()
        self.tv.delete(*self.tv.get_children())
        self.mostrartabla()

    def cargar(self, event):
        self.guardardatos()

    def guardar(self):
        self.eliminar.destroy()

    def cargardatos(self, event):
        self.button1.focus()

    def Mostrar(self):

        self.frame1 = Frame(self.eliminar)
        self.frame1.place(relx=0, rely=0.0, relheight=0.33, relwidth=1)
        self.frame1.config(bg="#b4cbca")

        self.frame2 = LabelFrame(self.eliminar)
        self.frame2.place(relx=0, rely=0.33, relheight=0.5, relwidth=1)
        self.frame2.config(bg="#deecec")

        self.frame3 = Frame(self.eliminar)
        self.frame3.place(relx=0, rely=0.83, relheight=0.17, relwidth=1)
        self.frame3.config(bg="#d5f4f4")

        self.label1 = Label(self.frame1, text="Eliminar Producto",
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

        # aqui se recibe el codigo de barras del producto
        self.label3 = Label(self.frame1, text="Codigo de barras",
                            anchor="w", bg="#b4cbca")
        self.label3.grid(padx=5, pady=5, row=1, column=1, sticky=E+W)

        self.entry_barras = Entry(self.frame1)
        self.entry_barras.grid(padx=5, pady=5, row=2,
                               column=1, sticky=E+W, ipady=5)
        self.entry_barras.focus()
        self.entry_barras.bind(
            '<Return>', self.cargardatos)

        self.button1 = Button(self.frame1, fg="white", bg="#009E20",
                              text="Modificar Producto", width=20, command=lambda: self.guardardatos(), cursor="hand2")
        self.button1.grid(padx=5, pady=5, row=5, column=5,
                          sticky=W+E, columnspan=3)
        self.button1.bind('<Return>', self.cargar)

        # en esta parte se controla la tabla
        self.scroll = Scrollbar(self.frame2)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.tv = ttk.Treeview(self.frame2, columns=(
            "Colum1", "Colum2", "Colum3", "Colum4"), yscrollcommand=self.scroll.set, selectmode="none")
        self.tv.pack(expand=True, fill=BOTH)
        self.scroll.config(command=self.tv.yview)
        self.tv.heading("#0", text="Codigo de barras", anchor=CENTER)
        self.tv.heading("Colum1", text="Nombre",
                        anchor=CENTER)
        self.tv.heading("Colum2", text="Precio de Compra",
                        anchor=CENTER)
        self.tv.heading("Colum3", text="Precio de Venta", anchor=CENTER)
        self.tv.heading("Colum4", text="Cantidad",
                        anchor=CENTER)
        self.mostrartabla()
        # aqui se muestra el total
        # self.Total = Label(self.frame3, text="Total",
        #                    bg="#BDEDBD", font=("Arial", 24))
        # self.Total.grid(row=0, column=0, sticky=E+W,
        #                 columnspan=3, padx=2, pady=2, ipady=5)

        # self.entry_total = Entry(self.frame3, font=("Arial", 24))
        # self.entry_total.grid(padx=5, pady=5, row=0, column=3,
        #                       columnspan=2, sticky=E+W, ipady=5)
        # self.entry_total.config(state="disable")
        self.finalizar = Button(self.frame3, fg="white", bg="#009E20",
                                text="Finalizar", width=20, command=lambda: self.guardar(), cursor="hand2")
        self.finalizar.place(relx=0.2, rely=0.2, relheight=0.5, relwidth=0.5)


class User(Frame):
    def __init__(self, master=None):
        super().__init__(master, width=320, height=220)
        self.master = master
        self.user = Toplevel()
        self.user.title("Login")
        self.user.geometry("350x220+500+200")
        # esto oculta la parte del titulo
        self.user.overrideredirect(True)
        self.Mostrar()

    def guardar(self):

        self.user.destroy()

    def mandar(self, event):
        self.guardar(self.entry_kilo.get(), self.opcion.get())

    def Mostrar(self):

        # Como StrinVar pero en entero

        r1 = Radiobutton(self.user, text="Normal",
                         value=1, variable=self.opcion, anchor="w")
        r1.grid(row=1, column=1, sticky=E+W)
        r2 = Radiobutton(self.user, text="Especial",
                         value=2, variable=self.opcion, anchor="w")
        r2.grid(row=2, column=1, sticky=E+W)
        r3 = Radiobutton(self.user, text="Milanesas",
                         value=3, variable=self.opcion, anchor="w")
        r3.grid(row=3, column=1, sticky=E+W)
        r4 = Radiobutton(self.user, text="Asado",
                         value=4, variable=self.opcion, anchor="w")
        r4.grid(row=4, column=1, sticky=E+W)
        self.k = Label(self.user,
                       text="Ingrese el kilaje de la comida", anchor="w")
        self.k.grid(padx=5, pady=5, row=5, column=1, columnspan=2, sticky=E+W)

        self.entry_kilo = Entry(self.user)
        self.entry_kilo.grid(padx=5, pady=5, row=6, column=1,
                             columnspan=2, sticky=E+W)
        self.entry_kilo.focus()
        self.entry_kilo.bind('<Return>', self.mandar)

        self.button2 = Button(self.user, fg="black", bg="#00EEFF",
                              text="OK", width=20, command=lambda: self.guardar(self.entry_kilo.get(), self.opcion.get()), cursor="hand2")
        self.button2.grid(padx=5, pady=5, row=7, column=1,
                          columnspan=3, sticky=W+E)
        # self.numero = int(self.entry_kilo)
