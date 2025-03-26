from PyQt5 import uic, QtWidgets
import psycopg2
import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas

dbname = 'conc'
user = 'postgres'
password = 'juki2010'
host = 'localhost'
port = '5432'

conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port)

cur = conn.cursor()

def send_data():
    line1 = formulario1.lineEdit.text()
    print("marca", line1)
    line2 = formulario1.lineEdit_2.text()
    print("nome", line2)
    line3 = formulario1.lineEdit_3.text()
    print("ano", line3)
    line4 = formulario1.lineEdit_4.text()
    print("preço", line4)
    line5 = formulario1.lineEdit_5.text()
    print("km", line5)
    line6 = formulario1.lineEdit_6.text()
    print("cambio", line6)
    line7 = formulario1.lineEdit_7.text()
    print("carroceria", line7)
    line8 = formulario1.lineEdit_8.text()
    print("cor", line8)
    line9 = formulario1.lineEdit_9.text()
    print("combustivel", line9)

    cursor=conn.cursor()
    comando_SQL="INSERT INTO base (marca,nome,ano,preco,km,cambio,carroceria,cor,combustivel) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    dados=(str(line1),str(line2),str(line3),str(line4),str(line5),str(line6),str(line7),str(line8),str(line9))    
    cursor.execute(comando_SQL,dados)
    conn.commit()
    formulario1.lineEdit.setText("")
    formulario1.lineEdit_2.setText("")
    formulario1.lineEdit_3.setText("")
    formulario1.lineEdit_4.setText("")
    formulario1.lineEdit_5.setText("")
    formulario1.lineEdit_6.setText("")
    formulario1.lineEdit_7.setText("")
    formulario1.lineEdit_8.setText("")
    formulario1.lineEdit_9.setText("")

def other_page():
    formulario2.show()
    cursor=conn.cursor()
    comando_SQL = "SELECT * FROM base"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    formulario2.tableWidget.setRowCount(len(dados_lidos))
    formulario2.tableWidget.setColumnCount(10)

    for i in range(0, len(dados_lidos)):
        for j in range(0,10):
            formulario2.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def generate_pdf():
    cursor=conn.cursor()
    comando_SQL = "SELECT * FROM base"
    cursor.execute(comando_SQL)
    dados_lidos=cursor.fetchall()
    y=0
    pdf = canvas.Canvas("carros_cadastrados.pdf")
    pdf.setFont("Times-Bold",25)
    pdf.drawString(200,800, "Carros cadastrados:")
    pdf.setFont("Times-Bold",18)
    pdf.drawString(10,750,"ID")
    pdf.drawString(110,750,"Marca")
    pdf.drawString(210,750,"Nome")
    pdf.drawString(360,750,"Ano")
    pdf.drawString(460,750,"Preço")



    for i in range (0,len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 -y ,str(dados_lidos[i][0]))
        pdf.drawString(110,750 -y ,str(dados_lidos[i][1]))
        pdf.drawString(210,750 -y ,str(dados_lidos[i][2]))
        pdf.drawString(360,750 -y ,str(dados_lidos[i][3]))
        pdf.drawString(460,750 -y ,str(dados_lidos[i][4]))


    
    pdf.save()
    messagebox.showinfo("PDF gerado com sucesso!")
        




app=QtWidgets.QApplication([])
formulario1=uic.loadUi("frame1.ui")
formulario2=uic.loadUi("frame2.ui")
formulario1.pushButton.clicked.connect(send_data)
formulario1.pushButton_2.clicked.connect(other_page)
formulario2.pushButton.clicked.connect(generate_pdf)



formulario1.show()
app.exec()
