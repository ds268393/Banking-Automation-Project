import gmail
import tkinter
from tkinter import *
from tkinter.ttk import Combobox #there is a submodule in tkinter module named as "ttk" and in this module there is a widget called "Combobox"
import time
import random
import sqlite3
import re
from PIL import ImageTk,Image
from tkinter import messagebox,filedialog
from threading import *
from tkinter.ttk import Style,Treeview,Scrollbar
import shutil
import os   #by using os module you can navigate 
            #inside files and folders

try:    
    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    curobj.execute("create table acn(acn_no integer primary key autoincrement,acn_name text,acn_pass text,acn_email text,acn_mob text,acn_bal float,acn_opendate text,acn_gender text,acn_type text)")
    conobj.close()
    print("table created")
except:
    #To prevent this error: "Operational Error: table acn
    #already exists".
    #If we run this programme more than once.
    print("table already exists")
    
try:
    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    curobj.execute("create table log (acn_no text,transaction_amount text,type text,datentime datetime,Beneficiary text)")
    conobj.commit()
    conobj.close()
except:
    print("Log table already created")
    


win=Tk()
win.state("zoomed")
win.configure(bg="pink")
win.title("Banking Automation Project")

win.resizable(width=False,height=False)
title=Label(win,text="Banking Automation",font=("Courier New",50,"bold","underline"),bg="pink")
title.pack()

dt=time.strftime("%d %B %Y,%A")
date=Label(win,text=dt,font=("arial",17,"bold"),bg="pink",fg="blue")
date.place(relx=.83,rely=.1)

def main_screen():
    global frm
    frm=Frame(win)  #Frame is kind of sub-window, parent
    #window is the master of this frame window.
    frm.configure(bg="powder blue")
    frm.place(relx=0,rely=0.15,relwidth=1,relheight=.85)
    
    def forgotpass():
        frm.destroy()
        forgotpass_screen()
    
    def newuser():
        frm.destroy()
        newuser_screen()
        
    def login():
        global gacn
        gacn=e_acn.get()
        pwd=e_pass.get()
        captcha=e_captcha.get()
        if len(gacn)==0 or len(pwd)==0 or len(captcha)==0:
            messagebox.showwarning("Validation","Empty fields are not allowed!!")
            return
        else:
            if f"{e_captcha.get()}.png"==files[counter%len(files)] or f"{e_captcha.get()}.jpg"==files[counter%len(files)]:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("select * from acn where acn_no=? and acn_pass=?",(gacn,pwd))
                tup=curobj.fetchone()
                conobj.close()
                if tup==None:
                    messagebox.showerror("No Record","No Record Found")
                else:
                    frm.destroy()
                    welcome_screen()
            else:
                messagebox.showwarning("Invalid Captcha","Please enter a valid captcha!!")
                return
        
        
    counter=random.randint(0,len(captcha_array))
    def next_captcha():
        nonlocal counter
        counter=random.randint(0,len(captcha_array))
        img_label.config(image=captcha_array[counter%len(captcha_array)])
        frm.update_idletasks()
         
    
    def clear(*args):
        for i in args:
            i.delete(0,"end")
        args[0].focus()
    
    lbl_acn=Label(frm,text="ACN",font=("arial",20,"bold"),bg="powder blue")
    lbl_acn.place(relx=.3,rely=.1)
    
    e_acn=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_acn.place(relx=.4,rely=.1)
    e_acn.focus()
    
    lbl_pass=Label(frm,text="Pass",font=("arial",20,"bold"),bg="powder blue")
    lbl_pass.place(relx=.3,rely=.2)
    
    e_pass=Entry(frm,font=("arial",20,"bold"),bd=5,show="*")
    e_pass.place(relx=.4,rely=.2)
    
    btn_login=Button(frm,text="login",font=("arial",20,"bold"),bd=5,command=login)
    btn_login.place(relx=.42,rely=.47)
    
    btn_clear=Button(frm,text="clear",font=("arial",20,"bold"),bd=5,command=lambda:clear(e_acn,e_pass,e_captcha))
    btn_clear.place(relx=.52,rely=.47)
    
    btn_fp=Button(frm,text="Forgot password? Click here",font=("arial",20,"underline"),bg="powder blue",fg="blue",bd=0,command=forgotpass)
    btn_fp.place(relx=.39,rely=.576)
    
    btn_new=Button(frm,text="Open New Account",font=("arial",20,"underline"),bg="powder blue",fg="blue",bd=0,command=newuser)
    btn_new.place(relx=.39,rely=.656)
    
    img_label=Label(frm,image=captcha_array[counter%len(files)])
    img_label.place(relx=.4,rely=.3)
    
    btn_refrsh=Button(frm,text='Refresh',bd=5,font=("arial",20,"bold"),width=6,height=1,command=next_captcha)
    btn_refrsh.place(relx=.6,rely=.31)
    
    e_captcha=Entry(frm,font=("arial",20,"bold"),bd=5,width=6)
    e_captcha.place(relx=.685,rely=.32)
    
    def advt():
        try:
            counter=0
            while 1>0:
                if counter==0:
                    img_label=Label(frm,image=advt_array[0],highlightthickness=5,highlightbackground="green")
                    img_label.place(relx=.0,rely=.78)
                    counter=1
                    time.sleep(2)
                else:
                    img_label.config(image=advt_array[counter%len(advt_array)])
                    counter+=1
                    time.sleep(2)
        except:
            pass
    t1=Thread(target=advt)
    t1.start()
    

 
files=os.listdir("captcha")
#print(files)  #['EEHfxw.jpg', 'Nqv6g38.jpg', 'oNVDPho.jpg']
captcha_array=[]
for file in files:
    #file_path=os.path.join("captcha",file)
    #print(file_path)
    img=Image.open(os.path.join("captcha",file))
    resized_img=img.resize((300,100))
    captcha_array.append(ImageTk.PhotoImage(resized_img))
#print(captcha_array)

filess=os.listdir("advt")
#print(filess)  #['1.png', '2.png', '3.png']
advt_array=[]
for filee in filess:
    imgg=Image.open(os.path.join("advt",filee))
    resized_imgg=imgg.resize((1535,155))
    advt_array.append(ImageTk.PhotoImage(resized_imgg))


def forgotpass_screen():
    frm=Frame(win)  #Frame is kind of sub-window, parent
    #window is the master of this frame window.
    frm.configure(bg="powder blue")
    frm.place(relx=0,rely=0.15,relwidth=1,relheight=.85)
    
    def back():
        frm.destroy()
        main_screen()
        
    counter=1
    def next_captcha():
        nonlocal counter
        img_label.config(image=captcha_array[counter%len(captcha_array)])
        frm.update_idletasks()
        counter+=1
    
    def clear(*args):
        for i in args:
            i.delete(0,"end")
        args[0].focus()
        
    def forgotpass_db():
        acn=e_acn.get()
        email=e_email.get()
        mob=e_mob.get()
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_pass from acn where acn_no=? and acn_email=? and acn_mob=?",(acn,email,mob))
        tup=curobj.fetchone()
        conobj.close()
        
        if tup==None:
            messagebox.showerror("Forgot Pass","Record Not Found")
        else:
            def sub_otp():
                if e_otp.get()==OTP:
                    messagebox.showinfo("Pwd recovered",f"Your acn no is {acn} and your password is {tup[0]}")
                    clear(e_acn,e_mob,e_email,e_captcha,e_otp)
                    next_captcha()
                else:
                    messagebox.showerror("Invalid OTP","Please enter a valid OTP")
            
            try:
                OTP=str(random.randint(1000,2000))
                connection=gmail.GMail("ds268393@gmail.com","ulbv phzz hnsn xajb")
                msg=gmail.Message(to=f"{email}",subject="Bank OTP mail",text=f"{OTP}")
                connection.send(msg)
                print("send successfully")
            except:
                messagebox.showerror("Invalid email ID or No connection","Either wrong email id provided during account opening\nor No internet connection available.")
            else:
                lbl_otp=Label(frm,text="OTP",font=("arial",20,"bold"),bg="powder blue")
                lbl_otp.place(relx=.7,rely=.58)
            
                e_otp=Entry(frm,font=("arial",20,"bold"),bd=5)
                e_otp.place(relx=.75,rely=.57)
                e_otp.focus()
                
                btn_subotp=Button(frm,text="Submit OTP",font=("arial",20,"bold"),bd=5,command=sub_otp)
                btn_subotp.place(relx=.75,rely=.67)
            
    lbl_fpscreen=Label(frm,text="This is forgot password screen (The OTP will be sent on Email ID)",font=("arial",20,"bold"),fg="blue",bg="powder blue",bd=5)
    lbl_fpscreen.pack()
    
    btn_new=Button(frm,text="Back",font=("arial",20,"bold"),fg="blue",bd=5,command=back)
    btn_new.place(relx=.0,rely=.0)
    
    lbl_acn=Label(frm,text="ACN",font=("arial",20,"bold"),bg="powder blue")
    lbl_acn.place(relx=.3,rely=.1)
    
    e_acn=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_acn.place(relx=.4,rely=.1)
    e_acn.focus()
    
    lbl_email=Label(frm,text="Email",font=("arial",20,"bold"),bg="powder blue")
    lbl_email.place(relx=.3,rely=.2)
    
    e_email=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_email.place(relx=.4,rely=.2)
    
    lbl_mob=Label(frm,text="Mob",font=("arial",20,"bold"),bg="powder blue")
    lbl_mob.place(relx=.3,rely=.3)
    
    e_mob=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_mob.place(relx=.4,rely=.3)
    
    img_label=Label(frm,image=captcha_array[0])
    img_label.place(relx=.4,rely=.4)
    
    btn_refrsh=Button(frm,text='Refresh',bd=5,font=("arial",20,"bold"),width=6,height=1,command=next_captcha)
    btn_refrsh.place(relx=.6,rely=.41)
    
    e_captcha=Entry(frm,font=("arial",20,"bold"),bd=5,width=6)
    e_captcha.place(relx=.685,rely=.42)
    
    btn_sub=Button(frm,text="Submit & Generate OTP",font=("arial",20,"bold"),bd=5,command=forgotpass_db)
    btn_sub.place(relx=.3,rely=.575)
    
    btn_clear=Button(frm,text="clear",font=("arial",20,"bold"),bd=5,command=lambda:clear(e_acn,e_mob,e_email,e_captcha))
    btn_clear.place(relx=.55,rely=.575)
    
    
    def advt():
        try:
            counter=0
            while 1>0:
                if counter==0:
                    img_label=Label(frm,image=advt_array[0])
                    img_label.place(relx=.0,rely=.78)
                    counter=1
                    time.sleep(2)
                else:
                    img_label.config(image=advt_array[counter%len(advt_array)])
                    counter+=1
                    time.sleep(2)
        except:
            pass
    t1=Thread(target=advt)
    t1.start()
    
def newuser_screen():
    frm=Frame(win)  #Frame is kind of sub-window, parent
    #window is the master of this frame window.
    frm.configure(bg="powder blue")
    frm.place(relx=0,rely=0.15,relwidth=1,relheight=.85)
    
    def back():
        frm.destroy()
        main_screen()
        
    counter=1
    def next_captcha():
        nonlocal counter
        img_label.config(image=captcha_array[counter%len(captcha_array)])
        frm.update_idletasks()
        counter+=1 #It searched the counter in outer 
        #function instead of the top level but if we use 
        #the "global" instead of "nonlocal" then it will 
        #search in the top level for counter var and no 
        #"counter" var defined there due to which no 
        #variable 'counter' is defined error will appear.
    
    def clear(*args):
        for i in args:
            i.delete(0,"end")
        args[0].focus()
        
    def newuser_db():
        name=e_name.get()
        pwd=e_pass.get()
        email=e_email.get()
        mob=e_mob.get()
        gender=cb_gender.get()
        acntyp=cb_acntyp.get()
        captcha=e_captcha.get()
        bal=0
        opendate=time.strftime("%d %B %Y,%A")
        
        xx=["",' ',None,"  ","----select----"]
        if name in xx or pwd in xx or gender in xx or acntyp in xx:
            messagebox.showerror("Empty fields","Empty fields are not allowed")
            return
        
        if len(mob)==10:
            pattern=re.compile("[6-9]\d{9}")
            f_match=re.fullmatch(pattern,mob)
            if f_match==None:
                messagebox.showerror("Invalid Mob!!","Please enter a valid mobile number!!")
                return
            else:
                pass
        else:
            messagebox.showerror("Invalid Mob!!","Please enter a valid mobile number!!")
            return
        

        pattern=re.compile("[a-zA-Z0-9_.\w]+@\w+\.\w+")
        f_match=re.fullmatch(pattern,email)
        if f_match==None:
            messagebox.showerror("Invalid email!!","Please enter a valid mail ID!!")
            return
        else:
            pass
        
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("insert into acn (acn_name,acn_pass,acn_email,acn_mob,acn_bal,acn_opendate,acn_gender,acn_type) values(?,?,?,?,?,?,?,?)",(name,pwd,email,mob,bal,opendate,gender,acntyp))
        conobj.commit()
        conobj.close()
        
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select max(acn_no) from acn")
        #print(curobj.fetchone())
        xx=((curobj.fetchone())[0])
        #print(xx)
        conobj.commit()  #optional
        conobj.close()
        
        messagebox.showinfo("New User",f"Account Created Successfully.\nYour Account no. is {xx}")
        clear(e_name,e_pass,e_email,e_mob,e_captcha,cb_gender,cb_acntyp)
        cb_gender.current(0)
        cb_acntyp.current(0)
        next_captcha()
        
    lbl_details=Label(frm,text="This is Open New Account screen",font=("arial",20,"bold"),fg="blue",bg="powder blue",bd=5)
    lbl_details.pack()
    
    btn_back=Button(frm,text="Back",font=("arial",20,"bold"),fg="blue",bd=5,command=back)
    btn_back.place(relx=.0,rely=.0)
    
    lbl_name=Label(frm,text="Name",font=("arial",20,"bold"),bg="powder blue")
    lbl_name.place(relx=.3,rely=.1)
    
    e_name=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_name.place(relx=.4,rely=.1)
    e_name.focus()
    
    lbl_Gender=Label(frm,text="Gender",font=("arial",20,"bold"),bg="powder blue")
    lbl_Gender.place(relx=.626,rely=.1)
    
    cb_gender=Combobox(frm,values=["----select----","Male","Female","Others"],state="readonly",font=("arial",20,"bold"))
    cb_gender.place(relx=.7,rely=.1)
    
    lbl_acntyp=Label(frm,text="ACN type",font=("arial",20,"bold"),bg="powder blue")
    lbl_acntyp.place(relx=.626,rely=.2)
    
    cb_acntyp=Combobox(frm,values=["----select----","Insta Saving Account","Jan Dhan Account"],state="readonly",font=("arial",20,"bold"))
    cb_acntyp.place(relx=.72,rely=.2)
    
    lbl_pass=Label(frm,text="Pass",font=("arial",20,"bold"),bg="powder blue")
    lbl_pass.place(relx=.3,rely=.2)
    
    e_pass=Entry(frm,font=("arial",20,"bold"),bd=5,show="*")
    e_pass.place(relx=.4,rely=.2)
    
    lbl_email=Label(frm,text="Email",font=("arial",20,"bold"),bg="powder blue")
    lbl_email.place(relx=.3,rely=.3)
    
    e_email=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_email.place(relx=.4,rely=.3)
    
    lbl_mob=Label(frm,text="Mob",font=("arial",20,"bold"),bg="powder blue")
    lbl_mob.place(relx=.3,rely=.4)
    
    e_mob=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_mob.place(relx=.4,rely=.4)
    
    img_label=Label(frm,image=captcha_array[0])
    img_label.place(relx=.4,rely=.5)
    
    btn_refrsh=Button(frm,text='Refresh',bd=5,font=("arial",20,"bold"),width=6,height=1,command=next_captcha)
    btn_refrsh.place(relx=.6,rely=.51)
    
    e_captcha=Entry(frm,font=("arial",20,"bold"),bd=5,width=6)
    e_captcha.place(relx=.685,rely=.52)
    
    btn_sub=Button(frm,text="Submit",font=("arial",20,"bold"),bd=5,command=newuser_db)
    btn_sub.place(relx=.42,rely=.675)
    
    btn_clear=Button(frm,text="clear",font=("arial",20,"bold"),bd=5,command=lambda:clear(e_name,e_pass,e_email,e_mob,e_captcha,cb_gender,cb_acntyp))
    btn_clear.place(relx=.52,rely=.675)
    
    def advt():
        try:
            counter=0
            while 1>0:
                if counter==0:
                    img_label=Label(frm,image=advt_array[0])
                    img_label.place(relx=.0,rely=.78)
                    counter=1
                    time.sleep(2)
                else:
                    img_label.config(image=advt_array[counter%len(advt_array)])
                    counter+=1
                    time.sleep(2)
        except:
            pass
    t1=Thread(target=advt)
    t1.start()


def welcome_screen():
    frm=Frame(win)  #Frame is kind of sub-window, parent
    #window is the master of this frame window.
    frm.configure(bg="powder blue")
    frm.place(relx=0,rely=0.15,relwidth=1,relheight=.85)
    
    def back():
        frm.destroy()
        main_screen()
        
    def updatepic():
        try:
            nonlocal imgtk
            img=filedialog.askopenfilename()
            shutil.copy(img,f"profile_pic/{gacn}.png")
            img=Image.open(f"profile_pic/{gacn}.png").resize((120,140))
            imgtk=ImageTk.PhotoImage(img)
            lbl_img.configure(image=imgtk)
        except:
            pass
        
    if(os.path.exists(f"profile_pic/{gacn}.png")):
        img=Image.open(f"profile_pic/{gacn}.png").resize((120,140))
        imgtk=ImageTk.PhotoImage(img)
    else:
        img=Image.open("profile_pic/default.png").resize((120,140))
        imgtk=ImageTk.PhotoImage(img)
    
    lbl_img=Label(frm,image=imgtk)
    lbl_img.place(relx=.925,rely=.1)
    
    btn_propic=Button(frm,text="Update Pic",font=("arial",15),bd=5,bg='powderblue',command=updatepic)
    btn_propic.place(relx=.925,rely=.32)
        
    def details():
        ifrm=Frame(frm,highlightbackground="black",highlightthickness=3)
        ifrm.configure(bg="white")
        ifrm.place(relx=.13,rely=.1,relwidth=.795,relheight=.6766)
        
        lbl_details=Label(ifrm,text="This is details screen",font=("arial",20,"bold"),fg="blue",bg="white",bd=5)
        lbl_details.pack()
        
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_no,acn_name,acn_email,acn_mob,acn_bal,acn_opendate,acn_gender,acn_type from acn where acn_no=?",(gacn,))
        tup=curobj.fetchone()
        conobj.close()
        
        lbl_info=Label(ifrm,text=f"ACN no: {tup[0]} \n\nName: {tup[1]} \n\nAcn Opening date: {tup[5]} \n\nEmail ID: {tup[2]}           Mobile: {tup[3]} \n\nBalance: {tup[4]} \n\nGender: {tup[6]} \n\nAcn Type: {tup[7]}",font=("arial",20),fg="black",bg="white",bd=5)
        lbl_info.place(relx=.02,rely=.1)
        
    details()
    
    def update():
        ifrm=Frame(frm,highlightbackground="black",highlightthickness=3)
        ifrm.configure(bg="white")
        ifrm.place(relx=.13,rely=.1,relwidth=.795,relheight=.6766)
        
        lbl_update=Label(ifrm,text="This is update screen",font=("arial",20,"bold"),fg="blue",bg="white",bd=5)
        lbl_update.pack()
        
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_name,acn_email,acn_mob,acn_gender,acn_type,acn_pass from acn where acn_no=?",(gacn,))
        tup=curobj.fetchone()
        conobj.close()

        lbl_name=Label(ifrm,text="Name",font=("arial",20,"bold"),bg="white")
        lbl_name.place(relx=.1,rely=.1)

        e_name=Entry(ifrm,font=("arial",20,"bold"),bd=5)
        e_name.place(relx=.2,rely=.1)
        e_name.insert(0,tup[0]) #tup[0] will be inserted at 0th index of the "e_name" entry field if something that is already written in the "e_name" will be shifted towards right side.
        e_name.focus()

        lbl_Gender=Label(ifrm,text="Gender",font=("arial",20,"bold"),bg="white")
        lbl_Gender.place(relx=.55,rely=.1)

        val_gender=["----select----","Male","Female","Others"]
        cb_gender=Combobox(ifrm,values=val_gender,state="readonly",font=("arial",20,"bold"))
        if tup[3] in val_gender:
            ind_gender=val_gender.index(tup[3])
        cb_gender.current(ind_gender)
        cb_gender.place(relx=.65,rely=.1)
    
        lbl_acntyp=Label(ifrm,text="ACN type",font=("arial",20,"bold"),bg="white")
        lbl_acntyp.place(relx=.53,rely=.25)

        val_acntyp=["----select----","Insta Saving Account","Jan Dhan Account"]
        cb_acntyp=Combobox(ifrm,values=val_acntyp,state="readonly",font=("arial",20,"bold"))
        if tup[4] in val_acntyp:
            ind_acntyp=val_acntyp.index(tup[4])
        cb_acntyp.current(ind_acntyp)
        cb_acntyp.place(relx=.65,rely=.25)

        lbl_pass=Label(ifrm,text="Pass",font=("arial",20,"bold"),bg="white")
        lbl_pass.place(relx=.1,rely=.25)

        e_pass=Entry(ifrm,font=("arial",20,"bold"),bd=5)
        e_pass.insert(0,tup[5])
        e_pass.place(relx=.2,rely=.25)

        lbl_email=Label(ifrm,text="Email",font=("arial",20,"bold"),bg="white")
        lbl_email.place(relx=.1,rely=.4)

        e_email=Entry(ifrm,font=("arial",20,"bold"),bd=5)
        e_email.insert(0,tup[1])
        e_email.place(relx=.2,rely=.4)
    
        lbl_mob=Label(ifrm,text="Mob",font=("arial",20,"bold"),bg="white")
        lbl_mob.place(relx=.1,rely=.55)

        e_mob=Entry(ifrm,font=("arial",20,"bold"),bd=5)
        e_mob.insert(0,tup[2])
        e_mob.place(relx=.2,rely=.55)
        
        def update_db():
            name=e_name.get()
            pwd=e_pass.get()
            email=e_email.get()
            gender=cb_gender.get()
            acntyp=cb_acntyp.get()
            mob=e_mob.get()
            
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("update acn set acn_name=?,acn_pass=?,acn_email=?,acn_mob=?,acn_gender=?,acn_type=? where acn_no=?",(name,pwd,email,mob,gender,acntyp,gacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update","Record updated successfully!!")
            welcome_screen()
        btn_update=Button(ifrm,text="Update",font=("arial",20,"bold"),bd=5,command=update_db)
        btn_update.place(relx=.47,rely=.7)
        
        
        
    def deposit():
        ifrm=Frame(frm,highlightbackground="black",highlightthickness=3)
        ifrm.configure(bg="white")
        ifrm.place(relx=.13,rely=.1,relwidth=.795,relheight=.6766)
        
        lbl_deposit=Label(ifrm,text="This is deposit screen",font=("arial",20,"bold"),fg="blue",bg="white",bd=5)
        lbl_deposit.pack()
        
        lbl_amt=Label(ifrm,text="Amount",font=("arial",20,"bold"),fg="black",bg="white")
        lbl_amt.place(relx=0.1,rely=0.2)
        
        e_amt=Entry(ifrm,font=("arial",20,"bold"),bd=5)
        e_amt.place(relx=0.2,rely=0.2)
        
        def deposit_db():
            try:
                amt=float(e_amt.get())
                if amt<0.1:
                    messagebox.showerror("Invalid amount","Invalid Amount Entered!!")
                else:
                    conobj=sqlite3.connect(database="bank.sqlite")
                    curobj=conobj.cursor()
                    curobj.execute("update acn set acn_bal=acn_bal+? where acn_no=?",(amt,gacn))
                    conobj.commit()
                    conobj.close()
                    
                    conobj=sqlite3.connect(database="bank.sqlite")
                    curobj=conobj.cursor()
                    curobj.execute("insert into log values (?,?,'Cr',datetime('now'),'self')",(gacn,amt))
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo("Amount deposited",f"Amount of Rupees {amt} is deposited successfully!!")
            except:
                messagebox.showerror("Invalid amount","Invalid Amount Entered!!")

        btn_depoamt=Button(ifrm,text="deposit amount",font=("arial",20,"bold"),bd=5,command=deposit_db)
        btn_depoamt.place(relx=0.3,rely=0.4)
        
    def withdraw():
        ifrm=Frame(frm,highlightbackground="black",highlightthickness=3)
        ifrm.configure(bg="white")
        ifrm.place(relx=.13,rely=.1,relwidth=.795,relheight=.6766)
        
        lbl_withdraw=Label(ifrm,text="This is withdraw screen",font=("arial",20,"bold"),fg="blue",bg="white",bd=5)
        lbl_withdraw.pack()
        
        lbl_amt=Label(ifrm,text="Amount",font=("arial",20,"bold"),fg="black",bg="white")
        lbl_amt.place(relx=0.1,rely=0.2)
        
        e_amt=Entry(ifrm,font=("arial",20,"bold"),bd=5)
        e_amt.place(relx=0.2,rely=0.2)
        e_amt.focus()
        
        def withdraw_db():
            try:
                amt=float(e_amt.get())
                if amt<0.1:
                    messagebox.showerror("Invalid amount","Invalid Amount Entered!!")
                else:
                    conobj=sqlite3.connect(database="bank.sqlite")
                    curobj=conobj.cursor()
                    curobj.execute("select acn_bal from acn where acn_no=?",(gacn,))
                    tup=curobj.fetchone()
                    conobj.commit()
                    conobj.close()
                    if amt<=tup[0]:
                        conobj=sqlite3.connect(database="bank.sqlite")
                        curobj=conobj.cursor()
                        curobj.execute("update acn set acn_bal=acn_bal-? where acn_no=?",(amt,gacn))
                        conobj.commit()
                        conobj.close()
                        
                        conobj=sqlite3.connect(database="bank.sqlite")
                        curobj=conobj.cursor()
                        curobj.execute("insert into log values (?,?,'Dr',datetime('now'),'self')",(gacn,amt))
                        conobj.commit()
                        conobj.close()
                        
                        messagebox.showinfo("Amount Withdrawal",f"Amount of Rupees {amt} is withdraw successfully!!")
                    else:
                        messagebox.showerror("Insufficient balance","Insufficient balance!!")
            except:
                messagebox.showerror("Invalid amount","Invalid Amount Entered!!")
        
        btn_withamt=Button(ifrm,text="Withdraw amount",font=("arial",20,"bold"),bd=5,command=withdraw_db)
        btn_withamt.place(relx=0.3,rely=0.4)
        
    def txnhist():
        ifrm=Frame(frm,highlightbackground="black",highlightthickness=3)
        ifrm.configure(bg="white")
        ifrm.place(relx=.13,rely=.1,relwidth=.795,relheight=.6766)
        
        lbl_txnhist=Label(ifrm,text="This is transaction history screen",font=("arial",20,"bold"),fg="blue",bg="white",bd=5)
        lbl_txnhist.pack()
    
        tv=Treeview(ifrm)
        tv.place(relx=0.05,rely=.1,height=425,width=800)
        
        style = Style()
        style.configure("Treeview.Heading", font=('Arial',15,'bold'),foreground='black')

        sb=Scrollbar(ifrm,orient='vertical',command=tv.yview)
        sb.place(x=850,y=48,height=425)
        tv.configure(yscrollcommand=sb.set)

        tv['columns']=('col1','col2','col3','col4','col5')

        tv.column('col1',width=100,anchor='c')
        tv.column('col2',width=200,anchor='c')
        tv.column('col3',width=150,anchor='c')
        tv.column('col4',width=150,anchor='c')
        tv.column('col5',width=150,anchor='c')
        

        tv.heading('col1',text='acn_no')
        tv.heading('col2',text='Transaction_Amt')
        tv.heading('col3',text='Type')
        tv.heading('col4',text='datentime')
        tv.heading('col5',text='Beneficiary')

        tv['show']='headings'
        
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute("select * from log where acn_no=?",(gacn,))
        

        for row in curobj:
            tv.insert("","end",values=(row[0],row[1],row[2],row[3],row[4]))
        conobj.close()
        
    def moneytrans():
        ifrm=Frame(frm,highlightbackground="black",highlightthickness=3)
        ifrm.configure(bg="white")
        ifrm.place(relx=.13,rely=.1,relwidth=.795,relheight=.6766)
        
        lbl_moneytrans=Label(ifrm,text="This is money transfer screen",font=("arial",20,"bold"),fg="blue",bg="white",bd=5)
        lbl_moneytrans.pack()
        
        lbl_amt=Label(ifrm,text="Amount",font=("arial",20,"bold"),fg="black",bg="white")
        lbl_amt.place(relx=0.13,rely=0.2)
        
        e_amt=Entry(ifrm,font=("arial",20,"bold"),bd=5)
        e_amt.place(relx=0.25,rely=0.2)
        e_amt.focus()
        
        lbl_to=Label(ifrm,text="Beneficiary acn no",font=("arial",20,"bold"),fg="black",bg="white")
        lbl_to.place(relx=0.02,rely=0.35)
        
        e_to=Entry(ifrm,font=("arial",20,"bold"),bd=5)
        e_to.place(relx=0.25,rely=0.35)
        
        def moneytrans_db():
            to_acn_no=e_to.get()
            amt=float(e_amt.get())
            
            if to_acn_no==gacn:
                messagebox.showwarning("Transfer","Sender and recipient's account number can't be same!!")
                return
            
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_bal from acn where acn_no=?",(gacn,))
            avail_bal=(curobj.fetchone())[0] #availble balance
            conobj.commit()
            conobj.close()
            
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_no from acn where acn_no=?",(to_acn_no,))
            acn_exist=curobj.fetchone()
            conobj.commit()
            conobj.close()
            
            if acn_exist==None:
                messagebox.showwarning("Transfer","To ACN does not exist")
                return
            if avail_bal>=amt:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("update acn set acn_bal=acn_bal+? where acn_no=?",(amt,to_acn_no))
                curobj.execute("update acn set acn_bal=acn_bal-? where acn_no=?",(amt,gacn))
                conobj.commit()
                conobj.close()
                
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("insert into log values (?,?,'Dr',datetime('now'),?)",(gacn,amt,to_acn_no))
                curobj.execute("insert into log values (?,?,'Cr',datetime('now'),'self')",(to_acn_no,amt))
                conobj.commit()
                conobj.close()
                
                messagebox.showinfo("Successful!!",f"Amount of {amt} transferred sucessfully to ACN no {to_acn_no}!!")
        btn_sendmoney=Button(ifrm,text="Send Money",font=("arial",20,"bold"),bd=5,command=moneytrans_db)
        btn_sendmoney.place(relx=0.3,rely=0.5)
    
    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    curobj.execute("select acn_name from acn where acn_no=?",(gacn,))
    tup=curobj.fetchone()
    conobj.close()
    
    lbl_wel=Label(frm,text=f"Welcome, {tup[0].title()}",font=("arial",20,"bold"),fg="blue",bg="powder blue",bd=5)
    lbl_wel.place(relx=.0,rely=.0)
    
    btn_logout=Button(frm,text="logout",font=("arial",20,"bold"),fg="blue",bd=5,command=back)
    btn_logout.place(relx=.925,rely=.0)
    
    btn_details=Button(frm,text="Details",bd=5,font=("arial",20,"bold"),width=10,height=1,command=details)
    btn_details.place(relx=0,rely=.1)
    
    btn_update=Button(frm,text="Update",bd=5,font=("arial",20,"bold"),width=10,height=1,command=update)
    btn_update.place(relx=0,rely=.2)
    
    btn_deposit=Button(frm,text="Deposit",bd=5,font=("arial",20,"bold"),width=10,height=1,command=deposit)
    btn_deposit.place(relx=0,rely=.3)
    
    btn_withdraw=Button(frm,text="Withdraw",bd=5,font=("arial",20,"bold"),width=10,height=1,command=withdraw)
    btn_withdraw.place(relx=0,rely=.4)
    
    btn_txnhist=Button(frm,text="Transaction\nHistory",bd=5,font=("arial",20,"bold"),width=10,command=txnhist)
    btn_txnhist.place(relx=0,rely=.5)
    
    btn_moneytrans=Button(frm,text="Money\nTransfer",bd=5,font=("arial",20,"bold"),width=10,command=moneytrans)
    btn_moneytrans.place(relx=0,rely=.647)
    
    def advt():
        try:
            counter=0
            while 1>0:
                if counter==0:
                    img_label=Label(frm,image=advt_array[0],highlightthickness=3,highlightbackground="green")
                    img_label.place(relx=.0,rely=.78)
                    counter=1
                    time.sleep(2)
                else:
                    img_label.config(image=advt_array[counter%len(advt_array)])
                    counter+=1
                    time.sleep(2)
        except:
            pass
    t1=Thread(target=advt)
    t1.start()


main_screen()
win.mainloop()
