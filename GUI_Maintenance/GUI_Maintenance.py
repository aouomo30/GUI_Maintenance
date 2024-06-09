from tkinter import *
from tkinter import messagebox
from tkinter import ttk
# from songline import Sendline
# token = 'VY9XswE1vPV2nA4vRzDjFXuBIrfWONl8iLF0IwBtP1V'
# messenger = Sendline(token)

# DATABASE
from db_maintenance import *

import csv
from datetime import datetime

def writecsv(record_list):
    with open('data.csv','a',newline='',encoding='utf-8') as file:
        fw = csv.writer(file)
        fw.writerow(record_list)

GUI = Tk()
GUI.title('Program ซ่อมบำรุง')
GUI.geometry('800x600+50+50')

FONT1 = ('Angsana New',25, 'bold')
FONT2 = ('Angsana New',15)

####### TAB ########
Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
T3 = Frame(Tab)
Tab.add(T1,text='ใบแจ้งซ่อม')
Tab.add(T2,text='ดูใบแจ้งซ่อม')
Tab.add(T3,text='สรุป')
Tab.pack(fill=BOTH,expand=1)


####################

L = Label(T1,text='ใบแจ้งซ่อม',font=FONT1)
L.place(x=100,y=0)

L = Label(T1,text='ชื่อผู้แจ้ง',font=FONT2)
L.place(x=30,y=50)
v_name = StringVar()

E1 = ttk.Entry(T1,textvariable=v_name,font=FONT2)
E1.place(x=150,y=50)

L = Label(T1,text='แผนก',font=FONT2)
L.place(x=30,y=100)
v_department = StringVar()

E2 = ttk.Entry(T1,textvariable=v_department,font=FONT2)
E2.place(x=150,y=100)

L = Label(T1,text='อุปกรณ์',font=FONT2)
L.place(x=30,y=150)
v_device = StringVar()

E3 = ttk.Entry(T1,textvariable=v_device,font=FONT2)
E3.place(x=150,y=150)

L = Label(T1,text='อาการเสีย',font=FONT2)
L.place(x=30,y=200)
v_problem = StringVar()

E4 = ttk.Entry(T1,textvariable=v_problem,font=FONT2)
E4.place(x=150,y=200)

L = Label(T1,text='หมายเลข',font=FONT2)
L.place(x=30,y=250)
v_number = StringVar()

E5 = ttk.Entry(T1,textvariable=v_number,font=FONT2)
E5.place(x=150,y=250)

L = Label(T1,text='เบอร์โทร',font=FONT2)
L.place(x=30,y=300)
v_tel = StringVar()

E6 = ttk.Entry(T1,textvariable=v_tel,font=FONT2)
E6.place(x=150,y=300)

def save():
    name = v_name.get()
    department = v_department.get()
    device = v_device.get()
    problem = v_problem.get()
    number = v_number.get()
    tel = v_tel.get()

    text = '\n' + 'ชื่อผู้แจ้ง: ' + name + '\n' #\n ขึ้นบรรทัดใหม่
    text = text + 'แผนก: ' + department + '\n'
    text = text + 'อุปกรณ์: ' + device + '\n'
    text = text + 'อาการเสีย: ' + problem + '\n'
    text = text + 'หมายเลข: ' + number + '\n'
    text = text + 'โทร: ' + tel + '\n'
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    tsid = str(int(datetime.now().strftime('%y%m%d%H%M%S')) + 212224236248)
    insert_mtworkorder(tsid,name,department,device,problem,number,tel)
    v_name.set('')
    v_department.set('')
    v_device.set('')
    v_problem.set('')
    v_number.set('')
    v_tel.set('')
    update_table()

    #datalist = [dt,name,department,device,problem,number,tel]
    #writecsv(datalist)

    #messenger.sendtext(text)
    #messagebox.showinfo('กำลังบันทึก...',text)

B = ttk.Button(T1, text='บันทึกใบแจ้งซ่อม',command=save)
B.place(x=180,y=350)

########## TAB 2 ################
header =  ['TSID','ชื่อ','แผนก','อุปกรณ์','อาการเสีย','หมายเลข','เบอร์โทรผู้แจ้ง']
headerw = [50,100,100,150,200,100,100]

mtworkorderlist = ttk.Treeview(T2,columns=header,show='headings',height=10)
mtworkorderlist.pack()

for h,w in zip(header,headerw):
    mtworkorderlist.heading(h,text=h)
    mtworkorderlist.column(h,width=w, anchor='center')

mtworkorderlist.column('TSID',anchor='e')  # จัดให้ชิดขวา  

def update_table():
    #clear ข้อมูลเก่า
    mtworkorderlist.delete(*mtworkorderlist.get_children())
    data = view_mtworkorder()
    for d in data:
        d = list(d) #แปลง Tuple เป็น list
        del d[0] # ลบ ID จาก database ออก
        mtworkorderlist.insert('','end',values=d)

#################################
update_table()
GUI.mainloop()
