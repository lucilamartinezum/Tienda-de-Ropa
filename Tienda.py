from tkinter import ttk #se usa esta libreria para diseñar la interfaz
from tkinter import *

import sqlite3 #conectar con la base de datos

class Product:

    db_name = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Lucila')

        frame = LabelFrame(self.wind, text='Register a new Product', fg='black')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Name Input
        Label(frame, text='Name: ', fg='purple').grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        # Price Input
        Label(frame, text='Price: ', fg='purple').grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        # Barcode Input
        Label(frame, text='Barcode: ', fg='purple').grid(row=3, column=0)
        self.barcode = Entry(frame)
        self.barcode.grid(row=3, column=1)

        # Button Add Product
        ttk.Button(frame, text='Save Product', command=self.add_product).grid(row=5, columnspan=2, sticky=W + E)

        # Output Messages
        self.message = Label(text='', fg='red')
        self.message.grid(row=4, column=0, columnspan=3, sticky=W + E)

        # Table
        self.tree = ttk.Treeview(height=10, columns=('price', 'barcode'))
        self.tree.grid(row=6, column=0, columnspan=3)
        self.tree.heading('#0', text='Name', anchor=CENTER)
        self.tree.heading('#1', text='Price', anchor=CENTER)
        self.tree.heading('#2', text='Barcode', anchor=CENTER)

        # Button
        ttk.Button(text='SELL', command=self.sell_product).grid(row=7, column=0, sticky=W + E)
        ttk.Button(text='EDIT', command=self.edit_product).grid(row=7, column=1, sticky=W + E)
        ttk.Button(text='DELETE', command=self.delete_product).grid(row=7, column=2, sticky=W + E)


        # Filling the Row
        self.get_products()

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):
        # Cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Quering data
        query ='SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=(row[2], row[3]))

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0 and len(self.barcode.get()) != 0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES( NULL, ?, ?, ?)'
            parameters = (self.name.get(), self.price.get(), self.barcode.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Product {} added Successfully'.format(self.name.get())
            self.name.delete(0, END) #vuelva a su estado inicial
            self.price.delete(0, END)
            self.barcode.delete(0, END)
        else:
            self.message['text'] = 'Name, Price and Barcode are Required'
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please Select a Product'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name,))
        self.message['text'] = 'Product {} deleted Successfully'.format(name)
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please Select a Product'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel() #abre una ventanita arriba
        self.edit_wind.title = 'Edit Product'

        # Old Name
        Label(self.edit_wind, text='Old Name: ', fg='purple').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=name), state='readonly').grid(row=0, column=2)
        # New Name
        Label(self.edit_wind, text='New Name: ', fg='purple').grid(row=1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)
        # Old Price
        Label(self.edit_wind, text='Old Price: ', fg='purple').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_price), state='readonly').grid(row=2, column=2)
        # New Price
        Label(self.edit_wind, text='New Price: ', fg='purple').grid(row=3, column=1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3, column=2)

        Button(self.edit_wind, text='Update', command=lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row=4, column=2)

    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product Set name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Product {} update successfully'.format(name)
        self.get_products()

    def sell_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please Select a Product'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name,))
        self.message['text'] = 'Product {} has been sold Successfully'.format(name)
        self.get_products()




