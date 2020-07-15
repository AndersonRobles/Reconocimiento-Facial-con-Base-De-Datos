from tkinter import *
import pandas as pd
import tkinter as tk
from playsound import playsound
from PIL import Image, ImageTk
import numpy as np
from tkinter import ttk
import sqlite3
import cv2
from PIL import Image
import os
import xlsxwriter
from datetime import date
from tkinter import messagebox
import sys
import random


#=====================Create Database=============================================
def createdb():                     
    conn = sqlite3.connect('aulavirtual.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (name TEXT , passs TEXT,sqltime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)")
    conn.commit()
    conn.close()
createdb()
#======================Adding new admin in database===============================
def saveadmin():
	name_err = name_entry.get()
	pass_err = pass_entry.get()
	if name_err == "":
		messagebox.showinfo("Entrada no válida "," El nombre de usuario no puede estar vacío")
	elif pass_err == "":
		messagebox.showinfo("Entrada no válida "," La contraseña no puede estar vacía")
	else:
		conn=sqlite3.connect("aulavirtual.db")
		c=conn.cursor()
		c.execute("INSERT INTO users(name,passs) VALUES(?,?) ",(name_entry.get(),pass_entry.get()))
		conn.commit()
		messagebox.showinfo("Información "," Se ha agregado un nuevo usuario")
#========================FetchingdataofAdminfromdatabase==========================
def loggin():
	while True:
		a=name2_entry.get()
		b=pass2_entry.get()
		with sqlite3.connect("aulavirtual.db") as db:
			#CONEXION CUENTA ADMINISTRADOR CON USUARI Y PASS CREADO
			cursor=db.cursor() 
			find_user= ("SELECT * FROM users WHERE name = ? AND passs = ?") 
			cursor.execute(find_user,[(a),(b)])
			results=cursor.fetchall()
		if results:
			for i in results:
				window.destroy()
#Conexion al aula virtual con idcard y Dni del estudiante.
		find_user2= ("SELECT * FROM alumno WHERE idCard = ? AND dni = ?")
		cursor.execute(find_user2,[(a),(b)])
		results=cursor.fetchall()
		if results:
			for i in results:
				window.destroy()

#==================Window2+CreateFrame+f1============Animation also================================================
				window2=Tk()
				#LA PARTE DEL ADMINISTRADOR
				f1=Frame(window2)
				#LA PARTE DE REGISTRAR ESTUDIANTE
				f2=Frame(window2)
				#LISTA DE ESTUDIANTES
				f3=Frame(window2)
				#PANEL DEL AULA VIRTUAL
				f4=Frame(window2)
				def swap(frame):
					frame.tkraise()
				for frame in(f1,f2,f3,f4):     #Se declara las 4 ventanas para que sea una sola medida
					frame.place(x=0,y=0,width=800,height=450)
				window2.geometry("800x450+420+170")
				window2.resizable(False, False)
				label3=Label(f1,text="ADMINISTRADOR ",font=("Times New Roman",17,"bold"),bg="grey16",fg="white",relief=SUNKEN)
				label3.pack(side=TOP,fill=X)

				label4=Label(f2,text="AULA VIRTUAL",font=("Times New Roman",12,"bold"),bg="grey16",fg="white")
				label4.pack(side=BOTTOM,fill=X)
				statusbar=Label(f1,text="AULA VIRTUAL",font=("Times New Roman",10,"bold"),bg="grey16",fg="white",relief=SUNKEN,anchor=W)
				statusbar.pack(side=BOTTOM,fill=X)

				class AnimatedGIF(Label, object):
					def __init__(self, master, path, forever=True):
						self._master = master
						self._loc = 0
						self._forever = forever
						self._is_running = False
						im = Image.open(path)
						self._frames = []
						i = 0
						try:
							while True:
								photoframe = ImageTk.PhotoImage(im.copy().convert('RGBA'))
								self._frames.append(photoframe)
								i += 1
								im.seek(i)
						except EOFError: pass
						self._last_index = len(self._frames) - 1
						try:
							self._delay = im.info['duration']
						except:
							self._delay = 100
						self._callback_id = None
						super(AnimatedGIF, self).__init__(master, image=self._frames[0])
					def start_animation(self, frame=None):
						if self._is_running: return
						if frame is not None:
							self._loc = 0
							self.configure(image=self._frames[frame])
						self._master.after(self._delay, self._animate_GIF)
						self._is_running = True
					def stop_animation(self):
						if not self._is_running: return
						if self._callback_id is not None:
							self.after_cancel(self._callback_id)
							self._callback_id = None
						self._is_running = False
					def _animate_GIF(self):
						self._loc += 1
						self.configure(image=self._frames[self._loc])
						if self._loc == self._last_index:
							if self._forever:
								self._loc = 0
								self._callback_id = self._master.after(self._delay, self._animate_GIF)
							else:
								self._callback_id = None
								self._is_running = False
						else:
							self._callback_id = self._master.after(self._delay, self._animate_GIF)
					def pack(self, start_animation=True, **kwargs):
						if start_animation:
							self.start_animation()
						super(AnimatedGIF, self).pack(**kwargs)
					def grid(self, start_animation=True, **kwargs):
						if start_animation:
							self.start_animation()
						super(AnimatedGIF, self).grid(**kwargs)
					def place(self, start_animation=True, **kwargs):
						if start_animation:
							self.start_animation()
						super(AnimatedGIF, self).place(**kwargs)
					def pack_forget(self, **kwargs):
						self.stop_animation()
						super(AnimatedGIF, self).pack_forget(**kwargs)
					def grid_forget(self, **kwargs):
						self.stop_animation()
						super(AnimatedGIF, self).grid_forget(**kwargs)
					def place_forget(self, **kwargs):
						self.stop_animation()
						super(AnimatedGIF, self).place_forget(**kwargs)
				if __name__ == "__main__":
					l = AnimatedGIF(f1, "./Resources/fondo.gif")
					l.pack()
				
				


				label4=Label(f3,text="Sistema de asistencia de reconocimiento facial",font=("Times New Roman",12,"bold"),bg="grey16",fg="white")
				label4.pack(side=BOTTOM,fill=X)
#================================Trian System===========================================================


				def trainsystem():
					recognizer = cv2.face.LBPHFaceRecognizer_create()
					path = 'dataset'
					if not os.path.exists('./recognizer'):
						os.makedirs('./recognizer')
					def getImagesWithID(path):
						imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
						faces = []
						IDs = []
						for imagePath in imagePaths:
							faceImg = Image.open(imagePath).convert('L')
							faceNp = np.array(faceImg,'uint8')
							ID = int(os.path.split(imagePath)[-1].split('.')[1])
							faces.append(faceNp)
							IDs.append(ID)
							cv2.imshow("training",faceNp)
							cv2.waitKey(10)
						return np.array(IDs), faces
					Ids, faces = getImagesWithID(path)
					recognizer.train(faces,Ids)
					recognizer.save('recognizer/trainingData.yml')
					statusbar['text']='Sistema entrenado....'
					messagebox.showinfo("Información","Entrenamiento de los estudiantes Finalizado")
					cv2.destroyAllWindows()
#==============================Detector/Attendence======================================================

				def markattendance():
					if not os.path.exists('./Attendance'):
							os.makedirs('./Attendance')
					statusbar['text']='Marcador de Asistencia....'
					conn = sqlite3.connect('aulavirtual.db')
					c = conn.cursor()
					#Datos con los rostros que hemos entrenados.
					messagebox.showinfo("Información","Si esta encendido su camara,presione ACEPTAR")
					fname = "recognizer/trainingData.yml"
					if not os.path.isfile(fname):
					  print("Porfavor,entrenar los datos primero")
					  exit(0)
					  #Detector de reconocimiento facial con un entrenamiento definido 
					face_cascade = cv2.CascadeClassifier('./Resources/haarcascade_frontalface_default.xml')
					cap = cv2.VideoCapture(0)
					recognizer = cv2.face.LBPHFaceRecognizer_create()
					recognizer.read(fname)
					while True:
					  ret, img = cap.read()
					  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
					  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
					  for (x,y,w,h) in faces:
					    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3)
					    ids,conf = recognizer.predict(gray[y:y+h,x:x+w])
					    c.execute("select name from alumno where id = (?);", (ids,))
					    result = c.fetchall()
					    name = result[0][0]
					    rname=str(name)
					    if conf < 50:
					      cv2.putText(img, name, (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2)
					      cv2.putText(img,'Presiona boton "Enter" id:'+name,(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
					    else:
					      cv2.putText(img, 'Rostro Desconocido', (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,400,0),2)
					  cv2.imshow('Asistencia de Alumnos',img)
					  k = cv2.waitKey(30) & 0xff
					  if k == 13:
					  	#c.execute("UPDATE employees set status='present' WHERE id=(?);",(ids,))
					  	c.execute("SELECT * FROM alumno")
					  	employee_result = c.fetchall()
					  	stat=str(employee_result)
					  	time=str(date.today())
					  	df=pd.DataFrame(employee_result, columns=['id', 'Nombre', 'Apellido', 'IdCard','Carrera', 'Telefono', 'Sede', 'Dni','Status'])
					  	datatoexcel = pd.ExcelWriter("./Attendance/Alumno Asistencia"+time+".xlsx", engine='xlsxwriter')
					  	df.to_excel(datatoexcel, index= False, sheet_name = "Sheet1")
					  	worksheet = datatoexcel.sheets['Sheet1']
					  	#df.assign(E="")
					  	#header_list=['F']
					  	#df = df.reindex(columns = header_list)
					  	worksheet.set_column('A:A', 8)
					  	worksheet.set_column('B:B', 20)
					  	worksheet.set_column('C:C', 25)
					  	worksheet.set_column('D:D', 20)
					  	worksheet.set_column('E:E', 20)
					  	worksheet.set_column('F:F', 20)
					  	df.loc[stat, 'Status'] = 'present'
					  	#df.at[0,'status']= 'present'
					  	#df.set_value(stat, 'E','present')
					  	#df.set_value(rname, 'status','present')
					  	datatoexcel.save()
					  	playsound('./Resources/sound2.mp3')
					  	break
					cap.release()
					conn.commit()
					conn.close()
					cv2.destroyAllWindows()
					messagebox.showinfo("Información","Asistencia Finalizada con Exito")

#================================VENTANA REGISTRO ALUMNO=================================================================

				label5=Label(f2,text="Datos de Estudiantes",font=("Times New Roman",22,"bold"),bg="grey16",fg="white")
				label5.pack(side=TOP,fill=X)
				label6=Label(f2,text="Nombre",font=("Times New Roman",12,"bold"))
				label6.place(x=70,y=70)
				entry6=StringVar()
				entry6=ttk.Entry(f2,textvariable=entry6)
				entry6.place(x=170,y=70)
				entry6.focus()

				label7=Label(f2,text="Apellido",font=("Times New Roman",12,"bold"))
				label7.place(x=350,y=70)
				entry7=StringVar()
				entry7=ttk.Entry(f2,textvariable=entry7)
				entry7.place(x=450,y=70)
				entry7.focus()

				label8=Label(f2,text="Id Card(Id Sesión)",font=("Times New Roman",12,"bold"))
				label8.place(x=42,y=110)
				entry8=StringVar()
				entry8=ttk.Entry(f2,textvariable=entry8)
				entry8.place(x=170,y=110)
			


				label9=Label(f2,text="Carrera",font=("Times New Roman",12,"bold"))
				label9.place(x=350,y=110)
				entry9=StringVar()
				combo=ttk.Combobox(f2,textvariable=entry9,width=15,font=("Times New Roman",10,"bold"),state='readonly')
				combo['values']=("Ingenieria de Sistemas Computacionales","Ingenieria Industrial","Ingenieria Ambiental","Ingenieria Empresarial","Ingenieria Civil","Contabilidad","Enfermeria","Derecho","Marketing","Idiomas","Administración")
				combo.place(x=450,y=110,width=290,height=20)


				label10=Label(f2,text="Telefono",font=("Times New Roman",12,"bold"))
				label10.place(x=70,y=145)
				entry10=StringVar()
				entry10=ttk.Entry(f2,textvariable=entry10)
				entry10.place(x=170,y=145)


				label11=Label(f2,text="Sede",font=("Times New Roman",12,"bold"))
				label11.place(x=350,y=145)
				entry11=StringVar()
				combo=ttk.Combobox(f2,textvariable=entry11,width=15,font=("Times New Roman",10,"bold"),state='readonly')
				combo['values']=("LIMA ESTE","BREÑA","LOS OLIVOS","CHORRILLOS")
				combo.place(x=450,y=145,width=290,height=20)

				label12=Label(f2,text="DNI(Password)",font=("Times New Roman",12,"bold"))
				label12.place(x=62,y=180)
				entry12=StringVar()
				entry12=ttk.Entry(f2,textvariable=entry12)
				entry12.place(x=170,y=180)
			  
				btn1w2=ttk.Button(f1,text="Registrar Alumno",command=lambda:swap(f2))
				btn1w2.place(x=100, y=80,width=150,height=30)

				btn2w2=ttk.Button(f1,text="Entrenar Sistema",command=trainsystem)
				btn2w2.place(x=600, y=80,width=150,height=30)

				btn3w2=ttk.Button(f1,text="Asistencia",command=markattendance)
				btn3w2.place(x=100, y=170,width=150,height=30)

#======================Record_images_with_database======================================

				def capture_images():
					conn = sqlite3.connect('aulavirtual.db')
					c = conn.cursor()
					sql = """;
					CREATE TABLE IF NOT EXISTS alumno (
								id integer unique primary key autoincrement,
								name text,apellido text,idcard text,carrera text,telefono text,sede text,dni text,Status text
					);
					"""
					c.executescript(sql)
					if not os.path.exists('./dataset'):
						os.makedirs('./dataset')
					uname=entry6.get()
					up1=uname.upper()
					ape=entry7.get()
					idc=entry8.get()
					car=entry9.get()
					tel=entry10.get()
					sed=entry11.get()
					dni=entry12.get()
					if uname=="":
						messagebox.showerror("Error","Ingrese Nombre del Estudiante")
					elif ape=="":
						messagebox.showerror("Error","Ingrese Apellido del Estudiante")
					elif idc=="":
						messagebox.showerror("Error","Ingrese ID CARD del Estudiante")
					elif car=="":
						messagebox.showerror("Error","Seleccione su Carrera")													
					elif sed=="":
						messagebox.showerror("Error","Seleccione una Sede")
					elif tel=="":
						messagebox.showerror("Error","Ingrese su numero telefónico")
					else:
						c.execute('INSERT INTO alumno (name,apellido,idcard,carrera,telefono,sede,dni) VALUES (?,?,?,?,?,?,?)', (up1,ape,idc,car,tel,sed,dni))
						uid = c.lastrowid

						face_classifier=cv2.CascadeClassifier("./Resources/haarcascade_frontalface_default.xml")

						def face_extractor(img):
							gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
							faces=face_classifier.detectMultiScale(gray,1.2,7)
							if faces is():
								return None
							for(x,y,w,h) in faces:
								cropped_face=img[y:y+h,x:x+w]
							return cropped_face
						cap=cv2.VideoCapture(0)
						count=0
#CAPTURAR LAS IMAGENES EN GRABAR ESTUDIANTE
						while True:
							ret,frame=cap.read()
							if face_extractor(frame) is not None:
								count+=1
								face=cv2.resize(face_extractor(frame),(400,400))
								face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
								file_name_path="dataset/"+up1+"."+str(uid)+"."+str(count)+".jpg"
								cv2.imwrite(file_name_path,face)
								cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
								cv2.imshow("Busqueda de Rostro",face)
							else:

								print("Cara no encontrada,Encienda su Cámara")

								cv2.destroyAllWindows
								messagebox.showinfo("Información","Cara no encontrada,Enfoque o encianda su Cámara")

								pass
								#TOTAL DE 70 IMAGENES
							if cv2.waitKey(1)==13 or count==70:
								break
						cap.release()
						conn.commit()
						conn.close()
						statusbar['text']='Estudiante a sido registrado correctamente....'
						cv2.destroyAllWindows
						messagebox.showinfo("Información","Se guardaron las imagenes respectivas")


				btn5w2=ttk.Button(f2,text="Grabar Estudiante",command=capture_images)
				btn5w2.place(x=170, y=240,width=130,height=30)

				btn4w2=ttk.Button(f2,text="Atras",command=lambda:swap(f1))
				btn4w2.place(x=3, y=40,width=50,height=30)
				def swap2(frame):
					frame.tkraise()

				btn7w2=ttk.Button(f3,text="Atras",command=lambda:swap(f1))
				btn7w2.place(x=3, y=40,width=50,height=30)

				btn6w2=ttk.Button(f1,text="Datos de los Estudiantes",command=lambda:swap2(f3))
				btn6w2.place(x=255, y=225,width=150,height=30)

#=========================Window2Frame4DevelopersPage=========================================

				label10=Label(f4,text="Panel Principal",font=("Times New Roman",22,"bold"),bg="grey16",fg="white")
				label10.pack(side=TOP,fill=X)
				label11=Label(f4,text="Aula Virtual",font=("Times New Romanial",12,"bold"),bg="grey16",fg="white")
				label11.pack(side=BOTTOM,fill=X)

				label10=Label(f4,text="Aula Virtual",font=("Times New Roman",12,"bold"))
				label10.place(x=75,y=150)

				def swap4(frame):

					frame.tkraise()
					statusbar['text']='Sistema De reconocimiento Facial'

				
				if __name__ == "__main__":
					l = AnimatedGIF(f4, "./Resources/fondo3.gif")
					l.pack()


			
				btn4w2=ttk.Button(f4,text="Back	",command=lambda:swap4(f1))
				btn4w2.place(x=3, y=40,width=50,height=30)
				label15=Label(f4,text="Hola Usuario",font=("Times New Roman",12,"bold"))
				label15.place(x=425,y=58)
				
				#entry15=StringVar()
				#entry15=ttk.Entry(f4,textvariable=entry15)
				#entry15.place(x=460,y=58)
				#entry15.focus()
				def swap3(frame):
					frame.tkraise()	


				btn9w2=ttk.Button(f1,text="Aula Virtual",command=lambda:swap3(f4))
				btn9w2.place(x=255, y=280,width=150,height=30)


				def quit():
					window2.destroy()


				btn9w2=ttk.Button(f1,text="Exit",command=quit)
				btn9w2.place(x=255, y=335,width=150,height=30)


#===========================FETCHDATABASEINLISTVIEW=========================================	


				def fetch():
					conn = sqlite3.connect("aulavirtual.db")
					cur = conn.cursor()
					cur.execute("SELECT * FROM alumno")
					rows = cur.fetchall()
					for row in rows:
						#la parte de lista_table esta mas adelante,donde se crea su respectiva tabla.
						List_Table.insert("", tk.END, values=row)
					conn.close()

#==========================FUNCION PARA ELIMINAR TABLA=========================================
				def dell():

					conn = sqlite3.connect("aulavirtual.db")
					cur = conn.cursor()
					cur.execute("DELETE  FROM alumno")
					conn.commit()
					conn.close()
					cv2.destroyAllWindows
					messagebox.showinfo("Información","Se elimino correctamente,volver a entrar y verificar cambios")



				btn8w2=ttk.Button(f3,text="Ver Registro",command=fetch)
				btn8w2.place(x=10, y=320,width=130,height=30)

				btn9w2=ttk.Button(f3,text="Eliminar Registro",command=dell)
				btn9w2.place(x=250, y=320,width=140,height=30)


#================================Frame3LISTVIEW==========================================


				label8=Label(f3,text="Lista de Estudiante",font=("Times New Roman",20,"bold"),bg="grey16",fg="white")
				label8.pack(side=TOP,fill=X)

				Detail_Frame=Frame(f3,bd=4,relief=RIDGE,bg="green")
				Detail_Frame.place(x=8,y=100,width=800,height=200)
				scroll_x=Scrollbar(Detail_Frame,orient=HORIZONTAL)
				scroll_y=Scrollbar(Detail_Frame,orient=VERTICAL)
				List_Table=ttk.Treeview(Detail_Frame,columns=("1","2","3","4","5","6","7","8"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
				scroll_x.pack(side=BOTTOM,fill=X)
				scroll_y.pack(side=RIGHT,fill=Y)
				scroll_x.config(command=List_Table.xview)
				scroll_y.config(command=List_Table.yview)
				List_Table.heading("1",text="ID")
				List_Table.heading("2",text="Nombre")
				List_Table.heading("3",text="Apellido")
				List_Table.heading("4",text="Id Card")
				List_Table.heading("5",text="Carrera")
				List_Table.heading("6",text="Telefono")
				List_Table.heading("7",text="Sede")
				List_Table.heading("8",text="DNI")
				List_Table['show']='headings'
				List_Table.column("1",width=20)
				List_Table.column("2",width=100)
				List_Table.column("3",width=100)
				List_Table.column("4",width=40)
				List_Table.column("5",width=150)
				List_Table.column("6",width=80)
				List_Table.column("7",width=80)
				List_Table.column("8",width=70)				
				List_Table.pack(fill=BOTH,expand=1)

				f1.tkraise()
				window2.mainloop()

			break
		else:
			messagebox.showerror("Error","Usuario o Contraseña Invalido")
			break



#======================MainLoginScreen============================================
window=Tk()
window.title("Iniciar Sesión")
Label1=Label(window,text="Iniciar Sesión",font=("Times New Roman",22,"bold"),bg="grey19",fg="white")
Label1.pack(side=TOP,fill=X)
Label2=Label(window,text="Aula Virtual",font=("Times New Roman",14,"bold"),bg="grey19",fg="white")
Label2.pack(side=BOTTOM,fill=X)
#====================LoginandSignupTabs====================================
nb=ttk.Notebook(window)
tab1=ttk.Frame(nb)
tab2=ttk.Frame(nb)
nb.add(tab1,text="Usuario")
nb.add(tab2,text="Crear Usuario")
nb.pack(expand=True,fill="both")
#=============Logintab=========================================
name2_label=Label(tab1,text="ID",font=("Times New Roman",12,"bold"))
name2_label.place(x=10,y=40)
name2_entry=StringVar()
name2_entry=ttk.Entry(tab1,textvariable=name2_entry)
name2_entry.place(x=90,y=40)
name2_entry.focus()

pass2_label=Label(tab1,text="Password",font=("Times New Roman",12,"bold"))
pass2_label.place(x=10,y=80)
pass2_entry=StringVar()
pass2_entry=ttk.Entry(tab1,textvariable=pass2_entry,show="*")
pass2_entry.place(x=90,y=80)


#=====================SignupTab===============================
name_label=Label(tab2,text="ID",font=("Times New Roman",12,"bold"))
name_label.place(x=10,y=40)
name_entry=StringVar()
name_entry=ttk.Entry(tab2,textvariable=name_entry)
name_entry.place(x=90,y=40)
name_entry.focus()
pass_label=Label(tab2,text="Password",font=("Times New Roman",12,"bold"))
pass_label.place(x=10,y=80)
pass_entry=StringVar()
pass_entry=ttk.Entry(tab2,textvariable=pass_entry,show="*")
pass_entry.place(x=90,y=80)

def clear():
	name_entry.delete(0,END)
	pass_entry.delete(0,END)
#===============AddUserButtons==============================================
btn1=ttk.Button(tab2,text="Guardar",command=saveadmin)
btn1.place(x=50,y=150)
btn2=ttk.Button(tab2,text="Limpiar",command=clear)
btn2.place(x=140,y=150)
#================LoginButtonMainwindow1======================================
btn3=ttk.Button(tab1,text="Iniciar",width=20,command=loggin)
btn3.place(x=87,y=150)


window.geometry("300x500+420+170")
window.resizable(False, False)
window.mainloop()
