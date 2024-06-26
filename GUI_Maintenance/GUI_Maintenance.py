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
GUI.geometry('1200x600+50+50')

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
headerw = [100,150,150,200,250,150,150]

mtworkorderlist = ttk.Treeview(T2,columns=header,show='headings',height=10)
mtworkorderlist.pack()

# ปรับขนาดฟอนต์และตารางให้ฬหญ่ขึ้น
style = ttk.Style()
style.configure('Treeview.Heading',padding=(10,10),font=('Angsana New',20,'bold'))
style.configure('Treeview',rowheight=25,font=('Angsana New',15))


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

### หน้าสำหรับแก้ไขข้อมูล ######
def EditPage_mtworkorder(event=None):
    select = mtworkorderlist.selection()
    output = mtworkorderlist.item(select)
    op = (output['values'])

    tsid = op[0]
    t_name = op[1]
    t_department = op[2]
    t_device = op[3]
    t_problem = op[4]
    t_number = op[5]
    t_tel = '0{}'.format(op[6])


    GUI2 = Toplevel()
    GUI2.title('หน้าแก้ไขข้อมูลใบแจ้งซ่อม')
    GUI2.geometry('500x500')

    # แทรก Tab 1
    
    L = Label(GUI2,text='ใบแจ้งซ่อม',font=FONT1)
    L.place(x=100,y=0)

    L = Label(GUI2,text='ชื่อผู้แจ้ง',font=FONT2)
    L.place(x=30,y=50)
    v_name2 = StringVar()
    v_name2.set(t_name)

    E1 = ttk.Entry(GUI2,textvariable=v_name2,font=FONT2)
    E1.place(x=150,y=50)

    L = Label(GUI2,text='แผนก',font=FONT2)
    L.place(x=30,y=100)
    v_department2 = StringVar()
    v_department2.set(t_department)

    E2 = ttk.Entry(GUI2,textvariable=v_department2,font=FONT2)
    E2.place(x=150,y=100)

    L = Label(GUI2,text='อุปกรณ์',font=FONT2)
    L.place(x=30,y=150)
    v_device2 = StringVar()
    v_device2.set(t_device)

    E3 = ttk.Entry(GUI2,textvariable=v_device2,font=FONT2)
    E3.place(x=150,y=150)

    L = Label(GUI2,text='อาการเสีย',font=FONT2)
    L.place(x=30,y=200)
    v_problem2 = StringVar()
    v_problem2.set(t_problem)

    E4 = ttk.Entry(GUI2,textvariable=v_problem2,font=FONT2)
    E4.place(x=150,y=200)

    L = Label(GUI2,text='หมายเลข',font=FONT2)
    L.place(x=30,y=250)
    v_number2 = StringVar()
    v_number2.set(t_number)

    E5 = ttk.Entry(GUI2,textvariable=v_number2,font=FONT2)
    E5.place(x=150,y=250)

    L = Label(GUI2,text='เบอร์โทร',font=FONT2)
    L.place(x=30,y=300)
    v_tel2 = StringVar()
    v_tel2.set(t_tel)

    E6 = ttk.Entry(GUI2,textvariable=v_tel2,font=FONT2)
    E6.place(x=150,y=300)

    def edit_save():
        name = v_name2.get()
        department = v_department2.get()
        device = v_device2.get()
        problem = v_problem2.get()
        number = v_number2.get()
        tel = v_tel2.get()

        update_mtworkorder(tsid,'name',name)
        update_mtworkorder(tsid,'department',department)
        update_mtworkorder(tsid,'device',device)
        update_mtworkorder(tsid,'problem',problem)
        update_mtworkorder(tsid,'number',number)
        update_mtworkorder(tsid,'tel',tel)

        update_table()
        GUI2.destroy()

    B = ttk.Button(GUI2, text='บันทึกใบแจ้งซ่อม',command=edit_save)
    B.place(x=180,y=350)

    GUI2.mainloop

mtworkorderlist.bind('<Double-1>',EditPage_mtworkorder)

def Delete_mtworkorder(event=None):
    select = mtworkorderlist.selection()
    output = mtworkorderlist.item(select)
    tsid = (output['values'][0]) # get only tsid

    check = messagebox.askyesno('ยืนยันการลบ','คุณต้องการลบข้อมูลใช่หรือไม่')
    print(check)
    if check == True:
        delete_mtworkorder(tsid)
        update_table()


mtworkorderlist.bind('<Delete>',Delete_mtworkorder)

update_table()
GUI.mainloop()
