from ConexaoBD import *
import os
import pickle
import xlwt
import cx_Oracle

from tkinter import filedialog

BD = ConexaoBD()
with BD.conectarBanco() as connection:
    cursor = connection.cursor()
    cursor
    cursor.execute("Select * from cliente")
    resultado = cursor.fetchall()

    a = cursor.description
    print(a[0])
    col_names = [row[0] for row in cursor.description]

    print(col_names)
