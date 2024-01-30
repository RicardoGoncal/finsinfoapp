import customtkinter as ctk
from PIL import Image
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class TtkService():
    
    def __init__(self, frame, columns, columns_name):
        self.frame = frame
        self.columns = columns
        self.columns_name = columns_name


    def criar_tabela(self):

        # Criando cabeçalho da tabela
        tv = ttk.Treeview(self.frame, columns=self.columns, show='headings', height=15)
        # tv.place(x=10, rely=.1)

        for i in range(len(self.columns_name)):
            tv.heading(i+1, text=self.columns_name[i])
            tv.column(i+1, anchor="c", width=165)

        style = ttk.Style()
        style.theme_use("default")
    
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading",
                    background=[('active', '#3484F0')])

        return tv