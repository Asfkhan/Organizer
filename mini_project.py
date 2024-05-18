import tkinter
from tkinter import *
from tkinter import ttk, messagebox
import mysql
import mysql.connector
asf = Tk()

def connect():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aptech@123",
        database="asf"
    )
    return conn

def showdata():
    for a in treeview.get_children():
            treeview.delete(a)
    abc = connect()
    dummy_cursor = abc.cursor()
    dummy_cursor.execute("SELECT * FROM employee_status")
    rows = dummy_cursor.fetchall()
    for a in rows:
        treeview.insert(parent='', index='end', values=a)
    showBtn.config(state=DISABLED)
    deptnoEnt.config(state=NORMAL)

clmns=("Dno","dname","location")
treeview = ttk.Treeview(asf,columns=clmns,show="headings")
treeview.heading("Dno", text="Dno",anchor=CENTER)
treeview.heading("dname", text="DName",anchor=CENTER)
treeview.heading("location", text="Location",anchor=CENTER)
treeview.grid(row=7, columnspan=8)

def register():
    try:
        new_deptno = deptnoEnt.get()
        new_var_deptName = deptNameEnt.get()
        new_Var_location = locationEnt.get()
        dummy = connect()
        c = dummy.cursor()
        c.execute("insert into employee_status values(" + new_deptno + ",'" + new_var_deptName + "','" + new_Var_location + "')")
        dummy.commit()
        mug1 = (new_deptno, new_var_deptName, new_Var_location)
        treeview.insert('', 'end', values=mug1)
        messagebox.showinfo("Information", "Record Inserted Successfully....")
        dummy.close()
    except:
        messagebox.showinfo("Alert","Enter Values to Register or Duplicate Entry!")

title1 = Label(asf, text="Employee Management System", fg="green", background="yellow", font="time 15 bold",
               anchor=CENTER)
title1.grid(row=1, columnspan=8, padx=50)

deptno = Label(asf, text="Enter DeptNO:", fg="white", background="blue")
deptno.grid(row=2, column=1, ipadx=40)

deptnoEnt = Entry(asf)
deptnoEnt.grid(row=2, column=3, pady=10)

deptName = Label(asf, text="Enter DeptName:", fg="white", background="blue")
deptName.grid(row=3, column=1, ipadx=30)

deptNameEnt = Entry(asf)
deptNameEnt.grid(row=3, column=3, pady=10)

location = Label(asf, text="Enter Location:", fg="white", background="blue")
location.grid(row=4, column=1, ipadx=40)
locationEnt = Entry(asf)
locationEnt.grid(row=4, column=3, pady=10)

registerBtn = Button(asf, text="Register", background="yellow",command=register)
registerBtn.grid(row=5, column=1)
def updateEMP(tree):

    try:
        a2 = deptNameEnt.get()
        a3 = locationEnt.get()
        selected_data = treeview.selection()[0]
        print(treeview.item(selected_data)['values'])
        uid = treeview.item(selected_data)['values'][0]
        update_query = "update employee_status set DeptName='"+a2+"',location='"+a3+"' where Deptno=%s"
        sel_data = [uid]
        new_deptno = sel_data.__str__()
        jug = connect()
        box = jug.cursor()
        box.execute(update_query,sel_data)
        jug.commit()
        mug = (new_deptno,a2,a3)
        for a in treeview.get_children():
            treeview.delete(a)
        treeview.insert('','end',values=mug)
        jug.close()
        messagebox.showinfo("Congrats","Data Updated Successfully!")
    except :
        messagebox.showinfo("Alert","Select Data to Update!")

updateBtn = Button(asf, text="Update", background="yellow",command=lambda : updateEMP(treeview))
updateBtn.grid(row=5, column=2)
def item_selected(event):
    deptnoEnt.delete(0,END)
    deptNameEnt.delete(0,END)
    locationEnt.delete(0,END)
    for selected_item in treeview.selection():
        item = treeview.item(selected_item)
        record = item['values']
        fgg = record.__str__()
        print(record)
        messagebox.showinfo('Information','Click on Update or Delete '+fgg)
        deptnoEnt.insert(0,record[0])
        deptNameEnt.insert(0,record[1])
        locationEnt.insert(0,record[2])
treeview.bind('<<TreeviewSelect>>', item_selected)
def deleteEMP(tree):
    try:
        selected_item = treeview.selection()[0]
        print(treeview.item(selected_item)['values'])
        uid =  treeview.item(selected_item)['values'][0]
        del_query = "delete from employee_status where Deptno=%s"
        sel_data = [uid]
        mug = connect()
        abc = mug.cursor()
        abc.execute(del_query,sel_data)
        mug.commit()
        treeview.delete(selected_item)
        if messagebox.YES:
            messagebox.showinfo("Data Information","Data Deleted Successfully!")
            messagebox.ABORT
        else:
            messagebox.ABORT
    except:
        messagebox.showinfo("ALert","Select Data to Delete!")
deleteBtn = Button(asf, text="Delete", background="yellow",command=lambda : deleteEMP(treeview))
deleteBtn.grid(row=5, column=3)

showBtn = Button(asf, text="ShowAll", background="yellow",command=showdata)
showBtn.grid(row=5, column=5, padx=40)

def clearall():
    deptnoEnt.config(state=NORMAL)
    for a in treeview.get_children():
        treeview.delete(a)
    showBtn.config(state=NORMAL)

clearBtn = Button(asf, text="Clear", background="yellow",command=clearall)
clearBtn.grid(row=5, column=4)

note = Label(asf, text="PLease Select one record below to update or delete", background="Blue", fg="White", font="bold")
note.grid(row=6, columnspan=8, ipadx=90, pady=20)


searchLabel = Label(text="Please Enter Dept-no:", background="blue", fg="white")
searchLabel.grid(row=8, columnspan=2, padx=20, pady=20)

searchLabelEnt = Entry(asf)
searchLabelEnt.grid(row=8, column=3)

def search():
    for a in treeview.get_children():
        treeview.delete(a)
    mug = connect()
    dummy_cursor = mug.cursor()
    dummy_cursor.execute("select * from employee_status where Deptno = "+searchLabelEnt.get()+"",)
    row = dummy_cursor.fetchmany()
    for a in row:
            treeview.insert(parent='', index='end', values=a)
seachbtn = Button(text="Seacrh",command=search)
seachbtn.grid(row=8,column=4)
asf.mainloop()
