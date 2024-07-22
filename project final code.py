import csv #csv module
import requests #http request module
import mysql.connector #mysql python connector
import tkinter as tk # tkinter
UI=tk.Tk() #user interface

#Variables 
#creating database
mydb=mysql.connector.connect(
    host='localhost',                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    user='root',
    password='Password'
)
mycursor=mydb.cursor()
mycursor.execute("DROP database IF EXISTS vacappointments")
mycursor.execute("create database vacappointments;")
mycursor.execute("use vacappointments;")
mycursor.execute("DROP TABLE  IF EXISTS appointments;")
mycursor.execute('CREATE TABLE appointments(DoctorName VARCHAR(255),StudentName VARCHAR(255),StudentGrade INTEGER(2),StudentClass VARCHAR(3),StudentRoll INTEGER(2), Slot INTEGER(1));')
sqlFormula="INSERT INTO appointments (DoctorName,StudentName,StudentGrade,StudentClass,StudentRoll,Slot) VALUES (%s,%s,%s,%s,%s,%s);"

def Book():
    #input from UI
    Data=(DoctorName_in.get(),StudentName_in.get(),StudentGrade_in.get(),#still in form of tkinter object
          StudentClass_in.get(),StudentRoll_in.get(),
          Slot_in.get())
    if '' in Data:
        Error['text']='Blank Field / Fields'
    else:
        with open("Doctors_log.csv", 'r') as csv_f:
            r = csv.reader(csv_f)
            #lists of objects
            details = [i for i in r]
            Doctors = [i[0] for i in details[1:]]
            phone = [i[1] for i in details[1:]]
            del r,details #removing to make program lighter
            
        #converting from tkinter object into int and str
        DoctorName = str(DoctorName_in.get())
        StudentName= str(StudentName_in.get())
        StudentGrade=int(StudentGrade_in.get())
        StudentClass= str(StudentClass_in.get())
        StudentRoll=int(StudentRoll_in.get())
        Slot=int(Slot_in.get())
        
        while True:
            #Details
            i = Doctors.index(DoctorName.lower())#finding the doctor
            print("Doctor: ",DoctorName,"\nPhone Number: ",phone[i])

            #SQL
            appoinment=(DoctorName,StudentName,StudentGrade,StudentClass,StudentRoll,Slot)
            #Inputting in database
            mycursor.execute(sqlFormula,appoinment)
            mydb.commit()
            url = "https://www.fast2sms.com/dev/bulk"
            phno = phone[i]
            text = "Dr."+str(DoctorName)+", you have a vaccination appointment with "+StudentName+" of class: "+str(StudentGrade)+StudentClass+" roll number: "+str(StudentRoll)+" slot: "+str(Slot)
            payload = f"sender_id=FSTSMS&message={text}&language=english&route=p&numbers={phno}"#connecting to website
            headers = {
            'authorization': "T1p5dPJaqxvA4syU0cRkwNHY8uSgnFEW923XfbQrItMlZGzDe7r4ahQFKAn9P5RXbMTIcykLUdzfC8oD", #special API key to send message via fast sms
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
            }
            response = requests.request("POST", url, data=payload, headers=headers)
            print("Dear",StudentName,", \nMESSAGE SUCCESFULLY SENT!")
            Error['text']='Booked'
            print("Thank you for using this portal to make your vaccination appointment.")
            break
        UI.destroy()
        
#labels for boxes
Header=tk.Label(text='Fill in data in the following fields')
DoctorName_label = tk.Label(text="Enter the Doctor Name:"); DoctorName_in = tk.Entry(UI)
StudentName_label=tk.Label(text="Enter the Student name:");StudentName_in=tk.Entry(UI)
StudentGrade_label=tk.Label(text="Enter the Student Grade:");StudentGrade_in=tk.Entry(UI)
StudentClass_label=tk.Label(text="Enter the Student section:");StudentClass_in=tk.Entry(UI)
StudentRoll_label=tk.Label(text="Enter the Student roll number:");StudentRoll_in=tk.Entry(UI)
Slot_label=tk.Label(text="Enter the slot (1--3:00 to 3:15,2--3:15 to 3:30,3--3:30 to 3:45,4--3:45 to 4:00):")
Slot_in=tk.Entry(UI)
Book_Button=tk.Button(UI,text='Book Meeting',command=Book)#book button
Error=tk.Label(UI)

#organizing widgets in blocks
Header.pack()
DoctorName_label.pack();DoctorName_in.pack()
StudentName_label.pack();StudentName_in.pack()
StudentGrade_label.pack();StudentGrade_in.pack()
StudentClass_label.pack();StudentClass_in.pack()
StudentRoll_label.pack();StudentRoll_in.pack()
Slot_label.pack();Slot_in.pack()
Book_Button.pack();Error.pack()
tk.mainloop()
