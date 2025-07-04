import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import pickle as pkl
import os
from tkcalendar import Calendar
from datetime import date
from transaction import *
import  matplotlib as plt
import numpy as numpy

class VerticalScrolledFrame(ttk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """
    def __init__(self, parent ,height,*args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,height=height,
                           yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=self.canvas.yview)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = ttk.Frame(self.canvas)
        interior_id = self.canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
        
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                self.canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)
              
    def configcanvas(self,w):
        size = (w, self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        self.canvas.config(width=w)
               
class Scrollablelistbox(Frame):
    def __init__(self,parent,var):
        Frame.__init__(self,parent)
        self.lstbox=Listbox(self,listvariable=var,selectmode=SINGLE)
        scrollbar = Scrollbar(self,orient=VERTICAL,command=self.lstbox.yview)
        self.lstbox['yscrollcommand'] = scrollbar.set
   
        self.lstbox.pack(side='left')
        scrollbar.pack(side='right', expand=True, fill=Y)

def chgunit(px): #used to convert screen pixels to screen unit
    r=px-13
    px=(r/7)+2
    return int(px)

class Notessection: #used to manage the notesection in eventbalancesheet
    
    def __init__(self,parent,title,sw,sdic,bc):
        self.translst=[]   #stores list of transaction
        self.seltranslst=[]  # stores selected transacation
        self.nonseltranslst=[]
        self.title=title
        self.sw=sw
        self.total=0
        self.secfra=Frame(parent,bg=bc)
        self.secfra.pack(side='left',padx=(0,3),pady=3)
        self.topfra=Frame(self.secfra,bg=bc)
        self.topfra.grid(row=0,column=0)
        titlab=Label(self.topfra,text=title,bg=bc,fg='black')
        titlab.pack(side='left')
        addbut=Button(self.topfra,text='+',command=self.addtrans,bg=bc,fg='black',bd=0)
        addbut.pack(side='right')
        translab=Label(self.secfra,text="Transaction",bg=bc,fg='black')
        translab.grid(row=1,column=0,pady=9)
        self.midfram=Frame(self.secfra)
        self.midfram.grid(row=2,column=0)
        headfra=Frame(self.midfram)
        headfra.grid(row=0,column=0,columnspan=3,sticky=W)
        desfra=Frame(headfra,width=sdic['notedes'])
        desfra.pack(side='left')
        desfra.pack_propagate(0)
        deslab=Label(desfra,text='Description')
        deslab.pack(anchor=CENTER)
        desfra.config(height=deslab.winfo_reqheight())
        amtfra=Frame(headfra,width=sdic['notedes'])
        amtfra.pack(side='left')
        amtfra.pack_propagate(0)
        amtlab=Label(amtfra,text='Amount')
        amtlab.pack(anchor=CENTER)
        amtfra.config(height=amtlab.winfo_reqheight())

        
        statuslab=Label(headfra,text='Status',width=5)
        statuslab.pack(side='left')
        fra=VerticalScrolledFrame(self.midfram,320)
        fra.grid(row=2,column=0,columnspan=3)
        self.transfra=fra.interior
        
        fra.configcanvas(sdic['notewid'])
       
        botfra=Frame(self.secfra,bg=bc)
        botfra.grid(row=3,column=0,columnspan=3)
        self.tot=Label(botfra,text='total '+title+'='+str(self.total),fg='black',bg=bc)
        self.tot.pack(anchor=CENTER,fill=X)
        
    def deletetrans(self,t): # deletes notes transaction in the notes section
        if(isinstance(t,NotesTransaction)):
            if(isinstance(t.opentrans,Transaction)):
                if(t.opentrans.transfra.winfo_exists()):
                    t.opentrans.dele.config(state=NORMAL)
                    t.opentrans.dele.invoke()
                else:
                    t.opentrans=0
                
            if(isinstance(t.closetrans,Transaction)):
                if(t.closetrans.transfra.winfo_exists()):
                    t.closetrans.dele.config(state=NORMAL)
                    t.closetrans.dele.invoke()
                else:
                    t.closetrans=0
        
            self.translst.remove(t)
                
            t.transfra.destroy()


    def addtrans(self): # creates and adds notestransaction in the notes section
        t=NotesTransaction(self.transfra,self.sw)
        t.dele.config(command=lambda:self.deletetrans(t))
        self.translst.append(t)
        return t
        
    def addtransdetails(self,des,amt,status):
        t=self.addtrans()
        t.loadinfo(des,amt,status)

    def statuscheck(self):  #checks status notes transaction is paid or not
        for t in self.translst:
            if(isinstance(t,NotesTransaction)):
                print(t.status)
                if(t.status==1):
                    self.seltranslst.append(t)
                else:
                    self.nonseltranslst.append(t)
    def findtotal(self): #find the total amount in a section
        self.total=0
        for i in self.translst:
            if(isinstance(i,NotesTransaction)):
                try:
                    self.total=self.total+int(i.amt.get())
                    
                except Exception as e:
                    print(e)
        self.tot.config(text='total '+self.title+'='+str(self.total))

class Notesectiondate:  #used to manage single notesection in monthly balancesheet
    def __init__(self,parent,title,curdate,m,y,sw,lst,sdic,bc):
        self.statuslst=lst
        self.curdate=curdate
        self.title=title
        self.sw=sw
        self.m=m
        self.y=y
        self.translst=[]   #stores list of transaction
        self.seltranslst=[]  # stores selected transacation
        self.nonseltranslst=[]
        self.total=0
        self.secfra=Frame(parent,bg=bc)
        self.secfra.pack(side='left',padx=(0,3),pady=3)
        self.topfra=Frame(self.secfra,bg=bc)
        self.topfra.grid(row=0,column=0)
        titlab=Label(self.topfra,text=title,bg=bc,fg='black')
        titlab.pack(side='left')
        self.addbut=Button(self.topfra,text='+',bd=0,bg=bc,fg='black')
        self.addbut.pack(side='right')
        translab=Label(self.secfra,text="Transaction",bg=bc,fg='black')
        translab.grid(row=1,column=0,pady=9)
        self.midfram=Frame(self.secfra) 
        self.midfram.grid(row=2,column=0)
        headfra=Frame(self.midfram)
        headfra.grid(row=0,column=0,columnspan=5,sticky=W)
        desfra=Frame(headfra,width=sdic['ndatedes'])
        desfra.pack(side='left')
        desfra.pack_propagate(0)
        deslab=Label(desfra,text='Description')
        deslab.pack(anchor=CENTER)
        desfra.config(height=deslab.winfo_reqheight())
        amtfra=Frame(headfra,width=sdic['ndatedes'])
        amtfra.pack(side='left')
        amtfra.pack_propagate(0)
        amtlab=Label(amtfra,text='Amount')
        amtlab.pack(anchor=CENTER)
        amtfra.config(height=amtlab.winfo_reqheight())
        opentitlab=Label(headfra,text='Open',font=('Arial',9),width=chgunit(sdic['ndateclose']))
        opentitlab.pack(side='left')
        closetitlab=Label(headfra,text='Close',font=('Arial',9),width=chgunit(sdic['ndateclose']))
        closetitlab.pack(side='left')
        statuslab=Label(headfra,text='Status',width=percensize(3,sw),font=('Arial',10))
        statuslab.pack(side='left')
        fra=VerticalScrolledFrame(self.midfram,320)
        fra.grid(row=1,column=0,columnspan=5)
        self.transfra=fra.interior
        fra.configcanvas(sdic['ndatewid'])
        
        
        botfra=Frame(self.secfra,bg=bc)
        botfra.grid(row=3,column=0,columnspan=3)
        self.tot=Label(botfra,text='total '+title+'='+str(self.total),fg='black',bg=bc)
        self.tot.pack(anchor=CENTER)
        
    def deletetrans(self,t): # deletes notes transaction in the notes section
        if(isinstance(t,NotesTransaactiondate)):
            print('dele is called')
            if(isinstance(t.opentrans,Transaction)):
                if(t.opentrans.transfra.winfo_exists()):
                    t.opentrans.dele.config(state=NORMAL)
                    t.opentrans.dele.invoke()
                else:
                    t.opentrans=0
                
            if(isinstance(t.closetrans,Transaction)):
                if(t.closetrans.transfra.winfo_exists()):
                    t.closetrans.dele.config(state=NORMAL)
                    t.closetrans.dele.invoke()
                else:
                    t.closetrans=0
            if(t in self.translst):
                self.translst.remove(t)
                
            t.transfra.destroy()


    def addtrans(self,open,ind): # creates and adds notestransaction in the notes section
        t=NotesTransaactiondate(self.transfra,open,self.m,self.y,self.sw,self.curdate,ind)
        t.dele.config(command=lambda:self.deletetrans(t))

        t.statusbut.config(command=lambda:t.statusfun(self.statuslst))
        self.translst.append(t)
        return t
        
    def addtransdetails(self,des,amt,status,open,ind):
        t=self.addtrans(open,ind)
        t.loadinfo(des,amt,status)
        return t

    def statuscheck(self):  #checks status notes transaction is paid or not
        for t in self.translst:
            if(isinstance(t,NotesTransaactiondate)):
                print(t.status)
                if(t.status==1):
                    self.seltranslst.append(t)
                else:
                    self.nonseltranslst.append(t)
    def findtotal(self): #used to find total in a section
        self.total=0
        for i in self.translst:
            if(isinstance(i,NotesTransaactiondate)):
                try:
                    if(len(i.amt.get())>0):
                        self.total=self.total+int(i.amt.get())
               
                except Exception as e:
                    pass
        self.tot.config(text='total '+str(self.title)+'='+str(self.total))

class Section: #used to manage a single transaction section
    

    def __init__(self,parent,title,bc,sw,sdic):
        self.sw=sw
        self.translist=[] #stores list of all transaction in a section
        self.total=0

        secfra=Frame(parent,bg=bc)
        secfra.pack(side='left')
        self.topfra=Frame(secfra,bg=bc)
        self.topfra.grid(row=0,column=1)
        self.title=title
        titlelab=Label(self.topfra,text=title,bg=bc,fg='black')
        titlelab.pack(side='left',anchor=CENTER)
        addbut=Button(self.topfra,text='+',bd=0,command=self.addtrans,fg='black',bg=bc)
        addbut.pack(side='right',padx=10)
        newfra=Frame(secfra)
        fra=VerticalScrolledFrame(newfra,320)
        self.midfra=fra.interior
        tranlab=Label(secfra,text="Transactions",bd=0,bg=bc,fg='black')
        tranlab.grid(row=1,column=1,sticky='n')
        headfra=Frame(newfra)
        headfra.grid(row=0,column=0,columnspan=2,sticky=W)
        desfra=Frame(headfra,width=sdic['transdes'])
        desfra.pack(side='left')
        desfra.pack_propagate(0)
        deslab=Label(desfra,text='Description')
        deslab.pack(anchor=CENTER)
        desfra.config(height=deslab.winfo_reqheight())
        amtfra=Frame(headfra,width=sdic['transdes'])
        amtfra.pack(side='left')
        amtfra.pack_propagate(0)
        amtlab=Label(amtfra,text='Amount')
        amtlab.pack(anchor=CENTER)
        amtfra.config(height=amtlab.winfo_reqheight())
        
      
    
    
    
        fra.grid(row=1,column=0,columnspan=2)
        newfra.grid(row=2,column=0,columnspan=3)
        fra.configcanvas(sdic['transwid'])
        
        botfra=Frame(secfra)
        botfra.grid(row=3,column=1)
        self.tot=Label(botfra,text='total '+title+'='+str(self.total),bg=bc,fg='black')
        self.tot.pack(anchor=CENTER,fill=X)
    def deletrans(self,t):  #deletes transaction from given section
        if(hasattr(t,'transfra')):
            t.transfra.destroy()
            self.translist.remove(t)
            
            
    def addtrans(self):  #adds transactions in the given section
        t=Transaction(self.midfra,self.sw)
        t.dele.config(command=lambda:self.deletrans(t))
        self.translist.append(t)
        return t
    def addtransdetails(self,des,amt): #adds transaction in the section from getting information from payabale or receivable
        t=self.addtrans()
        t.loadinfo(des,amt)
        return t

    def findtotal(self):#used to find total in a section
        total=0
        try:
            for i in self.translist:
                if(hasattr(i,'amt')):
                    print(i.amt.get())
                    total=total+int(i.amt.get())
            self.total=total

            self.tot.config(text='total '+str(self.title)+'='+str(self.total))
        except Exception as e:

            messagebox.showerror('Invalid amount','Enter valid amount values in '+self.title+' section with'+str(e)+' in date ')

            self.total=0
            

class tile:     #creating class with objects required  
    finalbalance=0
    def __init__(self,parent,date,bal,sw,sdic):
        self.seclst=[]
        self.canvas=Canvas(parent)
       
        self.main=Frame(self.canvas)
        self.canvas.create_window(0,0,window=self.main)
        self.main.pack()
        self.inibal=bal
        self.date=date
        self.topfra=Frame(self.main,bg='SlateGray4')
        self.topfra.pack(side='top',anchor=N,fill=X)
        datelabel=Label(self.topfra,text='date:'+date,bg='SlateGray4',fg='white')
        datelabel.pack(side='right',padx=10,pady=5)
        
        ballabel=Label(self.topfra,text='Initial balance:'+str(bal),bg='SlateGray4',fg='white')
        ballabel.pack(side='left',padx=10,pady=5) 
        self.inilab=ballabel
    
        transfra=Frame(self.main,bg='SlateGray4')
        transfra.pack(side='top')
        normtrans=Frame(transfra,bg='SlateGray4')
        normtrans.grid(row=0,column=0)
        self.notetrans=Frame(transfra)
        self.notetrans.grid(row=0,column=1)
        normtitle=Label(normtrans,text='Money transactions',bg='white',fg='black')
        normtitle.grid(row=0,column=0,columnspan=2,sticky=NSEW,padx=(0,3))
        
        creditlab=Label(normtrans,text='Credits',fg='black',bg='PaleGreen1')

        creditlab.grid(row=1,column=0,sticky=NSEW,padx=3,pady=(3,0))
        debitlab=Label(normtrans,text='Debits',fg='black',bg='IndianRed1')
        debitlab.grid(row=1,column=1,sticky=NSEW,padx=(0,3),pady=(3,0))
        creditframe=Frame(normtrans)
        creditframe.grid(row=2,column=0,padx=3,pady=(0,3))
        debitframe=Frame(normtrans)
        debitframe.grid(row=2,column=1,padx=(0,3),pady=(0,3))

        self.income=Section(creditframe,'Income','PaleGreen1',sw,sdic) #create income section
        self.ocredit=Section(creditframe,'Others','PaleGreen1',sw,sdic) #create other credit section
        self.expense=Section(debitframe,'Expense','IndianRed1',sw,sdic) #create expense section
       
        self.odebit=Section(debitframe,'Others','IndianRed1',sw,sdic) #create other debit section
        notetitle=Label(self.notetrans,text='Note Transactions',bg='white',fg='black')
        notetitle.grid(row=0,column=0,columnspan=2,sticky=NSEW)
        self.notetransframe=Frame(self.notetrans,bg='SlateGray4')
        self.notetransframe.grid(row=2,column=0,columnspan=2)
        
        self.seclst.append(self.income)
        self.seclst.append(self.expense)
        self.seclst.append(self.ocredit)
        self.seclst.append(self.odebit)
        self.updatefra=Frame(self.main,bg='SlateGray4')
        self.updatefra.pack(fill=X,side='top')
        self.finalballabel=Label(self.updatefra,text='Final balance:'+str(self.finalbalance)) #display final balance
        self.finalballabel.pack(side='right',padx=10)
        self.updatebut=Button(self.updatefra,text='update')
        self.updatebut.pack(side='top',anchor=CENTER)
        self.canvas.pack(side='top',anchor='center')

        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
    

            if self.main.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                self.canvas.config(width=self.main.winfo_reqwidth())
            if self.main.winfo_reqheight() != self.canvas.winfo_height():
                # Update the canvas's width to fit the inner frame.
                self.canvas.config(height=self.main.winfo_reqheight())
                print(self.main.winfo_reqheight())
            
        self.main.bind('<Configure>', _configure_interior)
    def updateinibal(self): #updates initial  balance
        self.inilab.config(text='Initial balance:'+str(self.inibal))
      
        
class eventtile(tile): #used to manage a event transactions
    def __init__(self,parent,name,date,bal,sw,sdic):
        self.evename=name
        
        self.evenfra=Frame(parent)
        namelab=Label(self.evenfra,text=name)
        namelab.pack(side='top')
        tile.__init__(self,self.evenfra,date,bal,sw,sdic)
        print(self.seclst)
        self.payable=Notessection(self.notetransframe,'payable',sw,sdic,'PaleTurquoise1') #create payable section
        self.receivable=Notessection(self.notetransframe,'receivable',sw,sdic,'LightYellow2') #create receivable section
       
        self.evenfra.pack()

    
        def updatebal(): #updates balances and other transactions
        
            self.payable.statuscheck()
            self.receivable.statuscheck()
            addpayableintrans()
            addreceivableintrans()
            self.income.findtotal()
            self.expense.findtotal()
            self.ocredit.findtotal()
            self.odebit.findtotal()
            self.receivable.findtotal()
            self.payable.findtotal()
            self.finalbalance=self.inibal+self.income.total+self.ocredit.total-self.odebit.total-self.expense.total
            print(self.finalbalance," ",self.inibal," ",self.income.total)
            self.finalballabel.config(text='Final balance:'+str(self.finalbalance))
           
           
            
        self.updatebut.config(command=updatebal)
        def updatetrans(t,des,amt):
            if(isinstance(t,Transaction)):
                t.des.config(state=NORMAL)
                t.amt.config(state=NORMAL)
                t.des.delete(0,END)
                t.des.insert(0,str(des))
                t.amt.delete(0,END)
                t.amt.insert(0,str(amt))
                t.des.config(state=DISABLED)
                t.amt.config(state=DISABLED)

        def addpayableintrans(): #adding payable in money transaction section
            for t in self.payable.translst:
                if(isinstance(t,NotesTransaction)):
                    if(isinstance(t.opentrans,Transaction)):
                        if(t.opentrans.transfra.winfo_exists()==False):
                            t.opentrans=0
                    if(isinstance(t.closetrans,Transaction)):
                        if(t.closetrans.transfra.winfo_exists()==False):
                            t.closetrans=0

                    if(t.opentrans!=0):
                        updatetrans(t.opentrans,t.des.get(),t.amt.get())
                    else:
                        i=self.ocredit.addtransdetails(t.des.get(),t.amt.get())
                        i.dele.config(state=DISABLED)
                        i.des.config(state=DISABLED)
                        i.amt.config(state=DISABLED)
                        t.opentrans=i
                    if(t.status==1):
                        if(t.closetrans!=0):
                            updatetrans(t.closetrans,t.des.get(),t.amt.get())
                        else:
                            i=self.odebit.addtransdetails(t.des.get(),t.amt.get())
                            i.dele.config(state=DISABLED)
                            i.des.config(state=DISABLED)
                            i.amt.config(state=DISABLED)
                            t.closetrans=i
                    else:
                        if(isinstance(t.closetrans,Transaction)):
                            t.closetrans.dele.config(state=NORMAL)
                            t.closetrans.dele.invoke()
                            t.closetrans=0
    
                
        def addreceivableintrans():   #adding receivable in money transaction section
            for t in self.receivable.translst:
                if(isinstance(t,NotesTransaction)):
                    if(isinstance(t.opentrans,Transaction)):
                        if(t.opentrans.transfra.winfo_exists()==False):
                            t.opentrans=0
                    if(isinstance(t.closetrans,Transaction)):
                        if(t.closetrans.transfra.winfo_exists()==False):
                            t.closetrans=0


                    if(t.opentrans!=0):
                         updatetrans(t.opentrans,t.des.get(),t.amt.get())
                    else:
                        i=self.odebit.addtransdetails(t.des.get(),t.amt.get())
                        i.des.config(state=DISABLED)
                        i.amt.config(state=DISABLED)
                        i.dele.config(state=DISABLED)
                        t.opentrans=i
                    if(t.status==1):
                        if(t.closetrans!=0):
                            updatetrans(t.closetrans,t.des.get(),t.amt.get())
                        else:
                            i=self.ocredit.addtransdetails(t.des.get(),t.amt.get())
                            i.dele.config(state=DISABLED)
                            i.des.config(state=DISABLED)
                            i.amt.config(state=DISABLED)
                            t.closetrans=i
                    else:
                        if(isinstance(t.closetrans,Transaction)):
                            t.closetrans.dele.config(state=NORMAL)
                            t.closetrans.dele.invoke()
                            t.closetrans=0
                    
       
    def save(self,filename,savewin): #saving the balancesheet as text and pickle 
        try:
            savewin.destroy()
            
            path=os.getcwd() #saving information as txt
            s=filename+'.txt'
            p=os.path.join(path,str(s))
            fin=open(p,'w+')
            i= self.income.translist
            s='date:'+date+'              initial balance='+str(self.inibal)+'\n'
            fin.write(s)
               
            for sec in self.seclst:
                if(hasattr(sec,'translist') and hasattr(sec,'title')):
                    n=len(sec.translist)
                    s=sec.title+':\n'
                    fin.write(s)
                    if(n>0):
                        for i in sec.translist:
                            print(i.des.get())
                            s='description:'+i.des.get()+'        '+'amount:'+i.amt.get()+'\n'
                            fin.write(s)
                               
                    else:
                        pass
                else:
                    pass
            fin.close()
               
                
        except Exception as e:
            print(e)
            print('error')
        try:
            s=filename+'.pickle'
            p=os.path.join(path,str(s))
            
            tiledetail={}
            tiledetail['cate']='eventtile'
            tiledetail['name']=self.evename
            tiledetail['inibal']=self.inibal
            tiledetail['date']=self.date
               
            paylst=[]
            for trans in self.payable.translst: #changed information into dictionaray and store in pickle file 
                if(isinstance(trans,NotesTransaction)):
                    transdic={}
                    transdic['des']=trans.des.get()
                    transdic['amt']=int(trans.amt.get())
                    transdic['status']=trans.status
                    paylst.append(transdic)
                
            recvlst=[]
            for trans in self.receivable.translst:
                if(isinstance(trans,NotesTransaction)):
                    transdic={}
                    transdic['des']=trans.des.get()
                    transdic['amt']=int(trans.amt.get())
                    transdic['status']=trans.status
                    recvlst.append(transdic)
            tiledetail['payable']=paylst
            tiledetail['receivable']=recvlst
            for sec in self.seclst:
                if(isinstance(sec,Section)):
                    translst=sec.translist
                    lst=[]
                    for trans in translst:
                        if(isinstance(trans,Transaction)):
                            if(trans.dele.cget('state')=='normal'):
                                transdic={}
                                transdic['des']=trans.des.get()
                                transdic['amt']=int(trans.amt.get())
                                lst.append(transdic)
                    tiledetail[sec.title]=lst
            fin=open(p,'wb+') 
            pkl.dump(tiledetail,fin)
            fin.close()
            self.updatebut.invoke()
            messagebox.showinfo('Info','Saved successfully')
            return filename     
                
        except Exception as e:
            messagebox.showerror('Error',e)
            print(e)
    def loadpkl(self,tiledetail): #loads data from pickle file
        for sec in self.seclst:
            if(isinstance(sec,Section)):
                lst=tiledetail[sec.title]
                for trans in lst:
                    sec.addtransdetails(trans['des'],trans['amt'])
            
        lst=tiledetail['payable']
        print(lst)
        for trans in lst:
            self.payable.addtransdetails(trans['des'],trans['amt'],trans['status'])
        lst=tiledetail['receivable']
        for trans in lst:
            self.receivable.addtransdetails(trans['des'],trans['amt'],trans['status'])
        

    
        self.updatebut.invoke()
        messagebox.showinfo('Info','Loaded successfully')


class tbalancesheet(tile): #a single balancesheet of monthly balanceheet
    def __init__(self,parent,day,month,year,inibal,sw,sdic):
    
        
        tile.__init__(self,parent,str(day)+'-'+str(month)+'-'+str(year),inibal,sw,sdic)
        self.curdate=day
        self.finpaylst=[] #save list of status changed payable transactions
        self.finrecvlst=[]  #save list of status changed receivable transactions
        self.payable=Notesectiondate(self.notetransframe,'payable',day,month,year,sw,self.finpaylst,sdic,'PaleTurquoise1')
        self.receivable=Notesectiondate(self.notetransframe,'receivable',day,month,year,sw,self.finrecvlst,sdic,'LightYellow2')
        self.paylst=[] #store manually added payable transactions
        self.recvlst=[] #store manually added receivable transactions
        self.totpayable=0
        self.totreceivable=0

    def updatebal(self): #update balances
        self.totpayable=0
        self.totreceivable=0
        try:
            for i in self.paylst:
                self.totpayable=self.totpayable+int(i.amt.get())
            for i in self.recvlst:
                self.totreceivable=self.totreceivable+int(i.amt.get())
    
        except Exception as e:
            print(e)
        
        self.income.findtotal()
        self.expense.findtotal()
         
        self.ocredit.findtotal()
        self.odebit.findtotal()
        self.receivable.findtotal()
        self.payable.findtotal()
        self.finalbalance=self.inibal+self.income.total+self.ocredit.total-self.odebit.total-self.expense.total #finds and saves final balance
    
        self.finalballabel.config(text='Final balance:'+str(self.finalbalance))

           
        
        


               
               