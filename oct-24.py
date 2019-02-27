import tkinter as tk

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import random
import string
import time;
import datetime
import fpdf
import matplotlib.pyplot as plt
import numpy as np
import csv
#----------------------------------------------------------------------------------
parent=Tk()
LARGE_FONT= ("Verdana", 12)
font1=("ARIAL",10,"bold")
font2=("ARIAL",12,"bold")
import sqlite3

#database connection--------------------------------------------------------------
conn = sqlite3.connect('product99.db')
print ("Opened Products database successfully")

#CREATE TABLE IF NOT EXISTS........
conn.execute('''CREATE TABLE IF NOT EXISTS mycart(NAME TEXT,COST  REAL,QTY INT);''')
print ("Table MYCART created successfully")

conn.execute('''CREATE TABLE IF NOT EXISTS p1(NAME TEXT,AMT  REAL);''')
print ("Table p1 created successfully")

conn.execute('''CREATE TABLE IF NOT EXISTS bill(NAME TEXT,COST  REAL,QTY INT,REC TEXT,DOS DATE,TOTAL_COST REAL);''')
print ("Table BILL created successfully")


#-----------------------------------------------------------------------------------

#FUCTONS ANS THEIR DEFINATION

def StartPage():                #Starting page 
        #creation of frames--------------------------------------------------------
        Tops= Frame(parent,width=1500,height=150,bd=5,relief="raise")
        Tops.pack()

        title=Label(Tops,text="Generalised Billing System!",font=("arial",40),bg="#A9D0F5")
        title.pack()

        f1= Frame(parent,width=(1500/10)*3,height=650-50,bd=10,bg="LIGHTBLUE",relief="raise")
        f1.pack(side="left")
        f2= Frame(parent,width=(1500/10)*4,height=650-50,bd=10,bg="LIGHTBLUE",relief="raise")
        f2.pack(side="left")
        f3= Frame(parent,width=(1500/10)*3,height=650-50,bd=10,bg="LIGHTBLUE",relief="raise")
        f3.pack(side="left")

        #FRAME1--------------------------------------------------------------------
        lab11=Label(f1,text='         ADMIN SECTION         ',font=("ARIAL",20,"bold"),bg="#F6E3CE")
        lab11.place(x=30,y=25)


        #FRAME2-------------------------------------------------------------------------
        listbox(f1,f2,f3)      #Creating Listbox
        
        global list1
        list1=[]
        


        lab12=Label(f2,text='         SALES SECTION         ',font=("ARIAL",20,"bold"),bg="#F6E3CE")
        lab12.place(x=85,y=25)
        
        L1 = Label(f2, text="ENTER ITEM", font=font1,height=2)
        E1 = Entry(f2, bd =5,font=('arial',16,'bold'), insertwidth=2, justify='center')
        L1.place(x=10,y=100)
        E1.place(x=100,y=100)

        Frame2(E1,f2,f3,f1)
        
        #FRAME3--------------------------------------------------------------------------------
        lab13=Label(f3,text='        BILL GENERATION       ',font=("ARIAL",20,"bold"),bg="#F6E3CE")
        lab13.place(x=30,y=25)

        mylist = Listbox(f3,selectmode="single",font=("arial",12),width=25)
        mylist.place(x=100,y=150)
        rec=Label(f3,font=("arial",13),width=25,bg="#5882FA")
        rec.place(x=100,y=100)
        
        ldate=Label(f3,font=("arial",13),width=25,bg="#5882FA")
        ldate.place(x=100,y=125)
        
        lab3=Label(f3,text="TOTAL COST",font=("arial",15,"bold"))
        lab3.pack()
        lab3.place(x=50,y=450)
        text1 = Text(f3,height=2,width=10)
        text1.place(x=200,y=450)
        r=0
        button1 = Button(f3, text="GENERATE",height=3,width=20,bg="#5882FA",font=font1,command=lambda :print_rec(r))
        button1.place(x=115,y=500)

        button2 = Button(f3, text="RESET",height=3,width=20,font=font1,bg="#5882FA",command=lambda:reset(f3,rec,ldate,f2,f1))
        button2.place(x=250,y=500)
#Creating list b0x in frame 2 
def listbox(frame1,frame2,frame3):         

        #FOR ADDING SCROLLING EFFECT (SCROLBAR)2
        scrollbar = Scrollbar(frame2,orient="vertical")
        scrollbar.pack( side="left", fill = "y" )
        scrollbar.place(x=150,y=150)

        mylist = Listbox(frame2, yscrollcommand = scrollbar.set ,selectmode="single",width=41)
        
        #RETRIVING DATA FROM DATABASE
        cursor = conn.execute("SELECT name, amt from p1")
        for row in cursor:
           print ("NAME = ", row[0])
           print ("Cost = ", row[1], "\n")
           mylist.insert("end",str(row[0]))

        mylist.pack( side="left", fill = "both" )
        mylist.place(x=100,y=135)
        scrollbar.config( command = mylist.yview )
        b2=Button(frame2,text='SELECT ITEM',font=font2,command=lambda :transfer_to_entrybox(mylist,frame2,frame3,frame1),bg="#5882FA",width=24)
        b2.place(x=100,y=295)      

        L1 = Label(frame1, text="ENTER PASSWORD", font=font1,height=2)
        E1 = Entry(frame1, bd =5,font=('arial',16,'bold'),show = '*', insertwidth=2, justify='center')
        L1.place(x=20,y=80)
        E1.place(x=150,y=80)

        submit=Button(frame1, text ="SUBMIT",font=font2,command=lambda :admin_menu(frame1,frame2,frame3,E1),height=2,width=10,bg="#5882FA",relief="raised",cursor="cross")
        submit.place(x=170,y=150)

        logout=Button(frame1, text ="LOGOUT",font=font2,command=lambda :logout_admin(frame1,frame2,frame3),height=2,width=10,bg="#5882FA",relief="raised",cursor="cross")
        logout.place(x=300,y=525)


#To eable admin section   ------------------------------------------------------------------------------------------------------     
def admin_menu(frame1,frame2,frame3,E1):
            if(E1.get()=="007"):

                        L2= Label(frame1,font=font2,height=2,width=25,bg="LIGHTBLUE")
                        L2.place(x=100,y=250)
                        
                        B1 = Button(frame1, text ="INSERT ITEMS",font=font2,command=lambda :newProduct(frame1,frame2,frame3),height=3,width=13,bg="#5882FA",relief="raised",cursor="cross")
                        B1.place(x=150,y=250)

                        B2 = Button(frame1, text ="REMOVE ITEMS",font=font2,command=lambda :remove_product(frame1,frame2,frame3),height=3,width=13,bg="#5882FA",relief="raised",cursor="cross")
                        B2.place(x=150,y=350)

                        B3 = Button(frame1, text ="ANALYSIS",font=font2,height=3,width=13, relief="raised",bg="#5882FA",command=analysis, cursor="exchange")
                        B3.place(x=150,y=450)
            else:
                        L2= Label(frame1,text="INVALID PASSWORD",font=font2,height=2,width=25)
                        L2.place(x=100,y=250)
                        while(E1.get()!=""):
                            E1.delete(0)
                        print("ENTER VALID PASSWORD")

def logout_admin(frame1,frame2,frame3):
        
        L2= Label(frame1,height=18,width=22,bg="LightBlue")
        L2.place(x=150,y=250)
        listbox(frame1,frame2,frame3)

#INSERT ITEMS----------------------------------------------------------------------------------------------
def  newProduct(frame,frame2,frame3):

        root=Tk()
        Tops= Frame(root,width=650,height=150,bd=5,relief="raise")
        Tops.pack()

        title=Label(Tops,text="INSERT NEW ITEMS",font=("arial",30))
        title.pack()

        f1= Frame(root,width=(650),height=500,bd=10,bg="LIGHTBLUE",relief="raise")
        f1.pack(side="left")

        L1 = Label(f1, text="ENTER ITEM", font=font1,height=2)
        E1 = Entry(f1, bd =5,font=('arial',16,'bold'), insertwidth=2, justify='center')
        L1.place(x=10,y=100)
        E1.place(x=100,y=100)

        L2 = Label(f1, text="ENTER COST", font=font1,height=2)
        E2 = Entry(f1, bd =5,font=('arial',16,'bold'), insertwidth=2, justify='center')
        L2.place(x=10,y=150)
        E2.place(x=100,y=150)

        a=E1.get()
        b=E2.get()
        print (a)
        print (b)
        add_button = Button(f1, text="ADD",height=3,width=20,font=font2,bg="#5882FA",command=lambda :add_it_to_database(E1,E2,frame,f1,frame2,frame3))
        add_button.place(x=220,y=300)
        
        button1 = Button(f1, text="Back to Main page",height=3,width=20,font=font2,bg="#5882FA",command=lambda :go_to_start(root))
        button1.place(x=220,y=400)

def add_it_to_database(E1,E2,frame,f1,f2,f3):
        print (E1.get())
        print (E2.get())
        a=E1.get()
        b=E2.get()
        p=E1.get().isdigit()
        q=E2.get().isdigit()
        print("P=",p)
        print("Q=",q)
        if (not p and q):
                print("CORRECT DATA INSERTED")
                if a!="" and b!="":
                        conn.execute("insert into p1 (NAME,AMT) values ( ?, ?)",(a,b))
                        conn.commit()
                        print ("DATA inserted");
                        listbox(frame,f2,f3)
                        E1.delete(0,END)
                        E2.delete(0,END)
                        global lab31
                        lab31=Label(f1,text="ITEM ADDED SUSSESFULLY",font=("arial",15))
                        lab31.place(x=200,y=250)
                        E1.bind("<Button-1>",some_callback)
                        E2.bind("<Button-1>",some_callback)
                else :
                        lab31=Label(f1,text="Please Enter Data Properly",font=("arial",15))
                        lab31.place(x=200,y=250)
                        E1.bind("<Button-1>",some_callback)
                        E2.bind("<Button-1>",some_callback)
        elif(p or not q):
                print("INCORRECT DATA INSERTED")
                lab31=Label(f1,text="INCORRECT DATA INSERTED",font=("arial",15))
                lab31.place(x=200,y=250)
                E1.bind("<Button-1>",some_callback)
                E2.bind("<Button-1>",some_callback)
        
        
def some_callback(event): # note that you must include the event as an arg, even if you don't use it.
        lab31.destroy()
        print ("hello")
def some_callback1(event): # note that you must include the event as an arg, even if you don't use it.
        print ("hello")
        l31.destroy()
        
#REMOVE ITEMS------------------------------------------------------------------------------------------------------
def remove_product(f1,f2,f3):
        root=Tk()
        Tops= Frame(root,width=650,height=150,bd=5,relief="raise")
        Tops.pack()

        title=Label(Tops,text="REMOVE ITEMS",font=("arial",30))
        title.pack()

        f1= Frame(root,width=(650),height=500,bd=10,bg="LIGHTBLUE",relief="raise")
        f1.pack(side="left")

        L1 = Label(f1, text="ENTER ITEM", font=font1,height=2)
        E1 = Entry(f1, bd =5,font=('arial',16,'bold'), insertwidth=2, justify='center')
        L1.place(x=10,y=100)
        E1.place(x=100,y=100)

        remove_button = Button(f1, text="REMOVE",height=3,width=20,font=font2,bg="#5882FA",command=lambda :rmv_prod(E1,f1,f2,f3))
        remove_button.place(x=220,y=300)

        button1 = Button(f1, text="Back to Main page",height=3,width=20,font=font2,bg="#5882FA",command=lambda :go_to_start(root))
        button1.place(x=220,y=400)


def rmv_prod(E1,f1,f2,f3):
        c=conn.execute("select NAME from p1 where NAME=?",(E1.get(),))
        flag=0
        for row in c:
            global lab33
            flag=1
            if row[0]:
                conn.execute("delete  from p1 where NAME=?",(E1.get(),))
                conn.commit()
                
                #FOR ADDING SCROLLING EFFECT (SCROLBAR)2
                scrollbar = Scrollbar(f2,orient="vertical")
                scrollbar.pack( side="left", fill = "y" )
                scrollbar.place(x=150,y=150)

                mylist = Listbox(f2, yscrollcommand = scrollbar.set ,selectmode="single",width=41)
                
                #RETRIVING DATA FROM DATABASE
                cursor = conn.execute("SELECT name, amt from p1")
                for row in cursor:
                   print ("NAME = ", row[0])
                   print ("Cost = ", row[1], "\n")
                   mylist.insert("end",str(row[0]))

                mylist.pack( side="left", fill = "both" )
                mylist.place(x=100,y=135)
                scrollbar.config( command = mylist.yview )
                b2=Button(f2,text='SELECT ITEM',font=font2,command=lambda :transfer_to_entrybox(mylist,f2,f3,f1),bg="#5882FA",width=24)
                b2.place(x=100,y=295)
                
                L1 = Label(f1, text="ENTER ITEM", font=font1,height=2)
                E1 = Entry(f1, bd =5,font=('arial',16,'bold'), insertwidth=2, justify='center')
                L1.place(x=10,y=100)
                E1.place(x=100,y=100)
                
                lab33=Label(f1,text="ITEM DELETED SUSSESFULLY",font=("arial",15))
                lab33.place(x=100,y=200)
                E1.bind("<Button-1>",some_callback3)
        if flag==0:
            L1 = Label(f1, text="ENTER ITEM", font=font1,height=2)
            E1 = Entry(f1, bd =5,font=('arial',16,'bold'), insertwidth=2, justify='center')
            L1.place(x=10,y=100)
            E1.place(x=100,y=100)
            lab33=Label(f1,text="ITEM NOT IN STORE",font=("arial",15))
            lab33.place(x=100,y=200)
            E1.bind("<Button-1>",some_callback3)
        
            
#messagebox.showinfo("Message","Your item has been delelted")    
def some_callback3(event): # note that you must include the event as an arg, even if you don't use it.
        print ("hello")
        lab33.destroy()
        
#ANALYSIS Part------------------------------------------------------------------------------------------------------
def  analysis():

        root=Tk()
        Tops= Frame(root,width=1000,height=150,bd=5,relief="raise")
        Tops.pack()

        title=Label(Tops,text="ANALYSIS",font=("arial",30))
        title.pack()

        f1= Frame(root,width=(700),height=400,bd=10,bg="LIGHTBLUE",relief="raise")
        f1.pack(side="left")
        
        button1 = Button(f1, text="BACK TO HOME",height=3,width=13,font=font2,bg="#5882FA",command=lambda :go_to_start(root))
        button1.place(x=280,y=300)

        B1 = Button(f1, text ="SALES PER DAY",command=sales_per_day,font=font2,height=3,width=13,bg="#5882FA",relief="raised",cursor="cross")
        B1.place(x=70,y=100)

        B2 = Button(f1, text ="Datewise Sale",command=today_sale,font=font2,height=3,width=13,bg="#5882FA", relief="raised", cursor="pirate")
        B2.place(x=500,y=100)
        
        B3 = Button(f1, text="Monthly",command=month,font=font2,height=3,width=13,bg="#5882FA", relief="raised",cursor="star")
        B3.place(x=280,y=100)
        
#SALES PER DAY------------------------------------------------------------------------------------------------------
def sales_per_day():
    print("SALES PER DAY")
    l1 = []
    l2 = []
    cursor = conn.execute("select dos,sum(total_cost) from bill group by dos")
    # month = datetime.date(1900, monthinteger, 1).strftime('%B')
    for row in cursor:
        m=int(str(row[0])[5:7])
        l1.append(str(row[0])[8:]+" "+datetime.date(1900,m, 1).strftime('%B')[0:3])
        l2.append(int(row[1]))
        print(row)
    max1=0
    ar3 = [float(numeric_string) for numeric_string in l2]
    for i in ar3:
            max1=max(i,max1)
    plt.xticks(np.arange(1, len(l1) + 1), l1,rotation="vertical")
    plt.xlim(0, max(10,len(l1)+2))
    plt.ylim(0, max1+20)
    plt.bar(np.arange(1, len(l1) + 1), ar3, alpha=0.5)
    plt.subplots_adjust(bottom=0.2)
    plt.title("Sales per day")
    plt.xlabel("DATE")
    plt.ylabel("Cost")
    plt.show()

#Particular day SALE------------------------------------------------------------------------------------------------------
def today_sale():

        root=Tk()
        Tops= Frame(root,bd=5,relief="raise")
        Tops.pack()

        title=Label(Tops,text="ENTER DATE",font=("arial",30))
        title.pack()

        f1= Frame(root,bd=10,bg="LIGHTBLUE",relief="raise")
        f1.pack(side="top")

        text1 = Text(f1,height=1,width=10,font=("bold"))
        text1.insert(END, "yyyy-mm-dd")
        text1.pack(side="top")
      
        E1 = Entry(f1, bd =5,font=('arial',16,'bold'),textvariable="yyyy-mm-dd", insertwidth=2, justify='center')
        E1.pack(side="top")
        
        button1 = Button(f1, text="SUBMIT",font=font2,bg="#5882FA",command=lambda :go_to_new(E1))
        button1.pack(side="top")
        

def go_to_new(E1):
        print(E1.get())
        l1 = []
        l2 = []
        now=datetime.datetime.now()
        s=str(now)
        print(s)
        cursor = conn.execute("select name,sum(qty) from bill where dos=? group by name ",(E1.get(),) )
        
        for row in cursor:

            l1.append(str(row[0]))
            l2.append(int(row[1]))
            print(row)
        max1 = 0
        ar3 = [float(numeric_string) for numeric_string in l2]
        for i in ar3:
            max1 = max(i, max1)
        plt.xticks(np.arange(1, len(l1) + 1), l1, rotation="vertical")
        plt.xlim(0, max(10, len(l1) + 2))
        plt.ylim(0, max1 + 20)
        plt.plot(np.arange(1, len(l1) + 1), ar3, "ro",alpha=0.5)
        plt.plot(np.arange(1, len(l1) + 1), ar3, alpha=0.5)

        plt.subplots_adjust(bottom=0.2)
        plt.title("Today's Total Sale")
        plt.xlabel("PRODUCT")
        plt.ylabel("Quantity")
        plt.show()

#MONTHLY SALE------------------------------------------------------------------------------------------------------
def month():
    data = []
    data1 = []
    w = []        
    count = 0
    k = []
    flag = 0
    
    fh = open('Book2.csv', 'r')
    csv_reader = csv.reader(fh)
    
    for row in csv_reader:
        if flag == 0:
            flag = 1
            continue
        
        if flag == 1:
            replacements = ('-', '/')
            for r in replacements:
                row[4] = row[4].replace(r, ' ')
                w = row[4].split()
            rate = w[1]
            data.append(rate)
            count = 0 
            flag = 2
            continue
        
        replacements = ('-', '/')
        for r in replacements:
            row[4] = row[4].replace(r, ' ')
            k = row[4].split()
        
        if rate == k[1]:
            count = count+float(row[5])
        else:
            rate = k[1]
            data.append(k[1])
            data1.append(count)
            

            print("COUNT=",k[1],count)
            count = 0
    data1.append(count)	
    fh.close()
    
    fig1,ax1 = plt.subplots()
  
    first_try={'01':"JAN",'02':"FEB",'03':"MAR",'04':"APR",'05':"MAY",'06':"JUN",'07':"JUL",'08':"AUG",'09':"SEP",'10':"OCT",'11':"NOV",'12':"DEC"}
    labels =[]
    
    for trial,value in first_try.items():
        for ran in data:
            if ran==trial:
                labels.append(first_try[trial])
                
    ax1.pie(data1,explode=None,autopct='%1.1f%%', startangle=0)
    ax1.axis('equal')
    plt.legend(labels)
    plt.show()
#------------------------------------------------------------------------------------------------
def transfer_to_entrybox(mylist,f2,f3,f1):
    val=[mylist.get(i) for i in mylist.curselection()]

    print(val)
    E1 = Entry(f2, bd =5,font=('arial',16,'bold'), insertwidth=2, justify='center')
    E1.insert(0, val)   
    E1.config(fg = 'black')
    E1.place(x=100,y=100)
    
    Frame2(E1,f2,f3,f1)
    l=Label(f2,text="",width=34,bg="LIGHTBLUE",font=("arial",15))
    l.place(x=195,y=350)

#Frame 2 functions and buttons  --------------------------------------------------------------------      
def Frame2(E1,f2,f3,f1):
        L2= Label(f2, text="QTY", font=('arial',10,'bold'),height=2,width=5)
        w = Spinbox(f2, from_=0, to=10,font=('arial',16,'bold'),width=5)
        L2.place(x=400,y=100)
        w.place(x=450,y=100)

        B = Button(f2, text ="ADD TO CART",command=lambda :add_it_to_myCart(E1,w,f2),font=font2,height=3,width=13,bg="#5882FA",relief="raised",cursor="cross")
        B.place(x=400,y=200)

        B1 = Button(f2, text ="MY CART",command=mycart,font=font2,height=3,width=13,bg="#5882FA",relief="raised",cursor="cross")
        B1.place(x=220,y=450)

        B2 = Button(f2, text ="CHECKOUT",command=lambda :generateBill(f3,f2,f1),font=font1,height=3,width=13,bg="#5882FA", relief="raised", cursor="pirate")
        B2.place(x=450,y=500)

        B3 = Button(f2, text="EXIT ",command=iExit,font=font1,height=3,width=13,bg="#5882FA", relief="raised",cursor="star")
        B3.place(x=10,y=500)

#ADD TO CART  ---------------------------------------------------------------------------------    
def add_it_to_myCart(E1,E2,f2):
        print ("NAME= "+E1.get())
        print ("Quantity= "+E2.get())
        a=E1.get()
        c=int(E2.get())
        print ("A =" ,a)
        print ("C =" ,c)
        
        flag=0
        print (list1)
        global l31
        for x in list1:
                if (x==E1.get()):
                        r=conn.execute("SELECT qty,cost FROM mycart where NAME=?",(E1.get(),))
                        for row in r:
                                ad1=int(row[0])
                                add_qty=ad1+c
                                print ("add_qty : " ,add_qty)
                        conn.execute("delete  from mycart where NAME=?",(E1.get(),))
                        conn.execute("insert into mycart (NAME,COST,QTY) values (?,?, ?)",(a,row[1],add_qty))
                        
                        conn.commit()
                        l31=Label(f2,text="ITEM ADDED SUSSESFULLY INTO CART",font=("arial",15))
                        l31.place(x=195,y=350)
                        E1.bind("<Button-1>",some_callback1)
                        E2.bind("<Button-1>",some_callback1)
                        flag=2
        if(E2.get() !="0" and flag!=2):
                
                print ("Dont ' insert Plzz select quantity  ")
                p=conn.execute("SELECT amt,name FROM p1 where NAME=?",(E1.get(),))
                
                for row in p:
                   flag=1
                   print ("COST = ", row[0])
                   print ("NAME = ", row[1])
                   
                if (flag==0):
                        print("NO PRODUCT FOUND")
                        l31=Label(f2,text="No Item Found",font=("arial",15))
                        l31.place(x=195,y=350)
                        E1.bind("<Button-1>",some_callback1)
                        E2.bind("<Button-1>",some_callback1)
                print ("DATA inserted");
                if (flag==1):
                        conn.execute("insert into mycart (NAME,COST,QTY) values (?,?, ?)",(a,row[0],c))
                        conn.commit()
                        list1.append(E1.get())
                        print ("LIST : " ,list1)
                        l31=Label(f2,text="ITEM ADDED TO CART",font=("arial",15))
                        l31.place(x=195,y=350)
                        E1.bind("<Button-1>",some_callback1)
                        E2.bind("<Button-1>",some_callback1)
        elif(flag!=2):
                 print ("can't insert Plzz select quantity  ")
                 l31=Label(f2,text="Please select Quantity ....",font=("arial",15))
                 l31.place(x=195,y=350)
                 E2.bind("<Button-1>",some_callback1)
                 E1.bind("<Button-1>",some_callback1)
        E1.configure(text="")


#MY CART  ------------------------------------------------------------------------------------
def  mycart():

        root=Tk()
        Tops= Frame(root,width=1500,height=150,bd=5,relief="raise")
        Tops.pack()

        title=Label(Tops,text="MY CART",font=("arial",30))
        title.pack()

        f1= Frame(root,width=(900),height=500,bd=10,bg="LIGHTBLUE",relief="raise")
        f1.pack(side="left")

        button1 = Button(f1, text="Back to Main page",height=3,width=20,bg="#5882FA",command=lambda :go_to_start(root))
        button1.place(x=220,y=400)

        L1 = Label(root, text="ENTER ITEM", font=font1,height=2)
        E1 = Entry(root, bd =5,font=('arial',16,'bold'), insertwidth=2, justify='center')
        L1.place(x=310,y=200)
        E1.place(x=400,y=200)

        
        button2 = Button(root, text="REMOVE ITEM",height=3,width=20,font=font2,bg="#5882FA",command=lambda :remove_item(E1,f1))
        button2.place(x=400,y=300)
        
        mycart_listbox(f1)
        
def mycart_listbox(frame1):
        scrollbar = Scrollbar(frame1,orient="vertical")
        scrollbar.pack( side="left", fill = "y" )
        scrollbar.place(x=174,y=170)

        mylist = Listbox(frame1, yscrollcommand = scrollbar.set ,selectmode="single",font=("arial",15))

        #RETRIVING DATA FROM DATABASE
        cursor = conn.execute("SELECT name, qty from mycart")
        for row in cursor:
           print ("NAME = ", row[0])
           print ("QTY = ", row[1], "\n")
           mylist.insert("end",(str(row[0])+"   ===> "+str(row[1])+" pcs"))

        #mylist.pack( side="left", fill = "both" )
        mylist.place(x=50,y=100)
        scrollbar.config( command = mylist.yview )

def remove_item(E1,f1):
                conn.execute("delete from mycart where NAME=?",(E1.get(),))
                mycart_listbox(f1)
                
def clear_cart():
        conn.execute("delete  from mycart");
        conn.commit()     

#Exit-------------------------------------------------------------------------------
def iExit():
        conn.execute("delete  from mycart");
        conn.commit()
        qExit = messagebox.askyesno("Billing System", "Do you want to exit the system?")
        if qExit > 0:
                parent.destroy()
                return


#CHECKOUT------------------------------------------------------------------------
def generateBill(f3,f2,f1):
        scrollbar = Scrollbar(f3,orient="vertical")
        scrollbar.pack( side="left", fill = "y" )
        scrollbar.place(x=174,y=170)

        mylist = Listbox(f3, yscrollcommand = scrollbar.set ,selectmode="single",font=("arial",12),width=25)

        now=datetime.datetime.now()
        s=str(now)
        print(s)

        p="REC"
        for j in range(3):
            digits="".join([random.choice(string.digits)])
            chars="".join([random.choice(string.ascii_letters)])
            p=p+digits+chars
        rec=Label(f3,text="REC_NO : "+p.upper(),font=("arial",13),width=25,bg="#5882FA")
        rec.place(x=100,y=100)
        
        ldate=Label(f3,text="Date : "+s[0:16],font=("arial",13),width=25,bg="#5882FA")
        ldate.place(x=100,y=125)
        r=p.upper()
        #RETRIVING DATA FROM DATABASE
        cursor = conn.execute("SELECT name,cost,qty from mycart")
        
        total_cost1=0
       
            
        
        for row in cursor:
           cost_of_product=0
           print ("NAME = ", row[0])
           print ("Cost = ", row[1])
           print ("QTY = ", row[2], "\n")
           cost_of_product=row[1]*row[2]
           total_cost1=total_cost1+cost_of_product
           mylist.insert("end",(str(row[0])+":= "+str(row[1])+" * "+str(row[2])+"  pcs = "+str(cost_of_product)+" /-"))
           conn.execute("insert into bill (NAME,COST ,QTY ,REC ,DOS,TOTAL_COST ) values (?,?,?,?,?,?)",(row[0],row[1],row[2],r,s[0:10],cost_of_product))
           conn.commit()
           a=row[0]
           b=row[1]
           c=row[2]
           d=r
           e=s[0:10]
           f=cost_of_product
           row = [[a,b,c,d,e,f]]
           with open(r'Book2.csv', 'a', newline='\n') as writeFile:
                writing = csv.writer(writeFile)
                writing.writerows(row)
           writeFile.close()
      
            
       
        mylist.place(x=100,y=150)
        scrollbar.config( command = mylist.yview )
        print (total_cost1)
        text1 = Text(f3,height=2,width=10,font=("HELVETICA",12))
        text1.place(x=200,y=450)
        text1.insert(END,str(total_cost1)+"/-")

        clear_cart()

        button1 = Button(f3, text="GENERATE",height=3,width=20,font=font1,bg="#5882FA",command=lambda :print_rec(r,total_cost1))
        button1.place(x=115,y=500)
        button1 = Button(f3, text="RESET",height=3,width=20,font=font1,bg="#5882FA",command=lambda:reset(f3,rec,ldate,f2,f1))
        button1.place(x=250,y=500)
        
        list1.clear()
        
        l=Label(f2,text="",width=34,bg="LIGHTBLUE",font=("arial",15))
        l.place(x=195,y=350)

#Frame 3---------------------------------------------------------------------
#GENERATE----------------------------------------------------------------------------------

def print_rec(r,t):
        l1=[]
        l2=[]
        
        p=conn.execute("select * from bill where  REC=?",(r,))
        for row in p:
                d=str(row[3])
                e=str(row[4])
        data11="\n-----------------------------------------------------------\n"
        data12="\n                 VISIT AGAIN\n"
        data13="                    MATAJI STORE \n                          BILL\n"
        data14="RECIPT NO : "+d+"\n"
        data15="DATE : "+e+"\n\n"
        data16="PRODUCT              COST                     QTY\n\n"
        data=data11+data13+data11+data14+data15+data11+data16
        l2=[data]
        data3=data11+data12+data11
        p=conn.execute("select * from bill where  REC=?",(r,))
        for row in p:
                a=str(row[0])
                b=str(row[1])
                c=str(row[2])
                a+=str(" "*(30-len(a)))
                b+=str(" "*(30-len(b)))
                c+=str(" "*(30-len(c)))
                l1=[a,b,c]
                l2.append(l1)
                l2.append("\n\n")
     
        data2="\n\nTOTAL COST : "+str(t)+data3
        l2.append(data2)
        print("LIST2 : ",l2)

        
        pdf=fpdf.FPDF(format='letter')
        pdf.add_page()
        pdf.set_font("ARIAL",size=12)
        for i in l2:
               for x in i:
                       pdf.write(5,str(x))
        rec=d+".pdf"
        pdf.output(rec)
        pdf.close()
       
        receipt = messagebox.showinfo("C:\\Users\\Jayesh Patil\\Desktop\\SDL_DBMS_PROJECT\\" , "Your receipt has been generated with "+rec)

#RESET----------------------------------------------------------------
def reset(f3,rec,ldate,f2,frame1):
        
        scrollbar = Scrollbar(f3,orient="vertical")
        scrollbar.pack( side="left", fill = "y" )
        scrollbar.place(x=174,y=170)

        mylist = Listbox(f3, yscrollcommand = scrollbar.set ,selectmode="single",font=("arial",12),width=25)
        mylist.place(x=100,y=150)
        scrollbar.config( command = mylist.yview )
        rec.destroy()
        ldate.destroy()
        text1 = Text(f3,height=2,width=10,font=("HELVETICA",12))
        text1.place(x=200,y=450)

        L2= Label(frame1,height=18,width=22,bg="LightBlue")
        L2.place(x=150,y=250)

        rec=Label(f3,font=("arial",13),width=25,bg="#5882FA")
        rec.place(x=100,y=100)
        
        ldate=Label(f3,font=("arial",13),width=25,bg="#5882FA")
        ldate.place(x=100,y=125)
        clear_cart()
        logout_admin(frame1,f2,f3)

#DESTROY TEMPORARY TKINTER WINDOW-----------------------------------------------------------------
def go_to_start(root):
    root.destroy()

#------------------------------------------------------------------------------------------------
#FUNCTTION CALL
c=StartPage()
#------------------------------------------------------------------------------------------------  


parent.mainloop()
conn.close()
