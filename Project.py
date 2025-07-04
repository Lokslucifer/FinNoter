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
import datetime as datetime
from transaction import *
from Sectionmod import *
import matplotlib.pyplot as plt
from PIL import Image,ImageTk
from random import randint
global curtile #stores the current frame
curtile=0

class balancetile: #creates and manage monthly balancesheet
    def __init__(self,parent,days,month,year,inibal,monthnum):
        self.sheetfra=Frame(parent)
        self.days=days
        self.ini=inibal
        self.m=month
        self.mn=monthnum
        self.y=year
        datefra=Frame(self.sheetfra)
        self.totpayable=0
        self.totreceivable=0
        self.rcolorlst=[]
        
        
        barbut=Button(datefra,text='I/E graph',command=self.disbargraph)
        barbut.pack(side='left',anchor='w',padx=10)
        paypiebut=Button(datefra,text='payable chart',command=lambda:self.dispaypiechart(self.tlist[self.days-1].payable.translst))
        paypiebut.pack(side='left',anchor='w',padx=10)
        recvpiebut=Button(datefra,text='recievable chart',command=lambda:self.disrecvpiechart(self.tlist[self.days-1].receivable.translst))
        recvpiebut.pack(side='left',anchor='w',padx=10)
        titlelab=Label(datefra,text=str(month)+' '+str(year)+' balancesheet',font=('Arial',14))
        titlelab.pack(side='top',anchor=CENTER)
        datebut=Button(datefra,text='1',bd=0,font=('Arial',12))
        datebut.pack(side='right')
        sellab=Label(datefra,text='Select a date:',font=('Arial',12))
        sellab.pack(side='right')
       
        datefra.pack(side='top',anchor='n',fill='x',padx=10)
        self.tlist=[] #save all tbalacesheets
        self.paylst=[] #saves all payable transaction
        self.recvlst=[]  #saves all receivable transaction
        self.finpaylst=[]  #saves all status changed payable transaction
        self.finrecvlst=[]  #saves all status changed receivable transaction
        self.compaylst={}   #saves all transactions belongs to a payable transaction
        self.comrecvlst={}  #saves all transactions belongs to a receivable transaction
        
        self.randlst=[]
        for i in range(0,1000,1):
            self.randlst.append(i)
        self.curdate=1
        datelst=[]
        t=tbalancesheet(self.sheetfra,1,monthnum,year,inibal,sw,sdic)
        t.payable.addbut.config(command=lambda:self.addnewpayable(self.tlist[self.curdate-1]))
        t.receivable.addbut.config(command=lambda:self.addnewreceivable(self.tlist[self.curdate-1]))
        t.updatebut.config(command=lambda:self.updatesheet(self.curdate-1))
        self.tlist.append(t)
        datelst.append(1)
        for i in range(1,days,1): #create tbalancesheets equal to number of days in a month
            t=tbalancesheet(self.sheetfra,i+1,monthnum,year,0,sw,sdic)
            t.payable.addbut.config(command=lambda:self.addnewpayable(self.tlist[self.curdate-1]))
            t.receivable.addbut.config(command=lambda:self.addnewreceivable(self.tlist[self.curdate-1]))
            t.updatebut.config(command=lambda:self.updatesheet(self.curdate-1))
        
            t.canvas.pack_forget()
            datelst.append(i+1)
            self.tlist.append(t)
        
        
        def createdatelistbox(): #date list box used to select date
            datevar=Variable(value=datelst)
            datewin=Toplevel(self.sheetfra)
            datewin.protocol("WM_DELETE_WINDOW", DISABLED)
            lstbox=Listbox(datewin,listvariable=datevar,selectmode=SINGLE)
            d=sellab.winfo_pointerxy()
            dw=datewin.winfo_reqwidth()
            dh=datewin.winfo_reqheight()
            datewin.geometry(('%dx%d+%d+%d')%(dw,dh,d[0]-200,d[1]+10))

            lstbox.pack()
            datebut.config(state=DISABLED)
       
            def selectdate(event):
                self.tlist[self.curdate-1].canvas.pack_forget()
                datebut.config(state=NORMAL)
                self.updatesheet(self.curdate-1)
                
                ind=lstbox.curselection()[0]
                self.curdate=ind+1

                self.curdate=int(self.curdate)
                datebut.config(text=str(self.curdate))
                datewin.destroy()
                if(isinstance(self.tlist[self.curdate-1],tile)):
                    self.tlist[self.curdate-1].canvas.pack()
            lstbox.bind('<<ListboxSelect>>',selectdate)
        datebut.config(command=createdatelistbox)
        self.sheetfra.pack()
    def addnewpayable(self,t): #add new payable
        if(isinstance(t,tbalancesheet)):
            trans=t.payable.addtrans(self.curdate,self.randlst[0])
            t.paylst.append(trans)
            if(isinstance(trans,NotesTransaactiondate)):
                trans.dele.config(command=lambda:self.delepaytrans(trans))
            

        
            
    
            del self.randlst[0]
            return trans
    def addnewreceivable(self,t): #adds new receivable
        if(isinstance(t,tbalancesheet)):
        
            trans=t.receivable.addtrans(self.curdate,self.randlst[0])
            t.recvlst.append(trans)
            if(isinstance(trans,NotesTransaactiondate)):
                trans.dele.config(command=lambda:self.delerecvtrans(trans))

            del self.randlst[0]
            return trans
    def delerecvtrans(self,t): #deletes a receivable transaction
    
        sheet=self.tlist[self.curdate-1]
        
        if(isinstance(t,NotesTransaactiondate)):
            if(t in sheet.finrecvlst):
                
                sheet.finrecvlst.remove(t)
        
            if(t.ind in self.comrecvlst):
                
                
                if(isinstance(t.opentrans,Transaction)):
                    t.opentrans.dele.config(state=NORMAL)
                    t.opentrans.dele.invoke()
                if(isinstance(t.closetrans,Transaction)):
                    t.closetrans.dele.config(state=NORMAL)
                    t.closetrans.dele.invoke()

                lst=self.comrecvlst[t.ind]
                n=len(lst)
                for i in range(1,n,1):
                    trans=lst[i]
                    if(isinstance(trans,NotesTransaactiondate)):
                        trans.dele.config(state=NORMAL)
                    
                        trans.dele.invoke()

                del self.comrecvlst[t.ind]
                self.randlst.append(t.ind)
            if(isinstance(sheet,tbalancesheet)):
                sheet.receivable.deletetrans(t)
            sheet.recvlst.remove(t)

    def delepaytrans(self,t): #deletes a payable transaction
    
        sheet=self.tlist[self.curdate-1]
        
        if(isinstance(t,NotesTransaactiondate)):
            if(t in sheet.finpaylst):
            
                sheet.finpaylst.remove(t)
            if(t.ind in self.compaylst):
                
                
                if(isinstance(t.opentrans,Transaction)):
                    t.opentrans.dele.config(state=NORMAL)
                    
                    t.opentrans.dele.invoke()
                if(isinstance(t.closetrans,Transaction)):
                    t.closetrans.dele.config(state=NORMAL)
                    t.closetrans.dele.invoke()

                lst=self.compaylst[t.ind]
                n=len(lst)
                for i in range(1,n,1):
                    trans=lst[i]
                    if(isinstance(trans,NotesTransaactiondate)):
                        trans.dele.config(state=NORMAL)
                    
                        trans.dele.invoke()

                del self.compaylst[t.ind]
                self.randlst.append(t.ind)
            if(isinstance(sheet,tbalancesheet)):
                sheet.payable.deletetrans(t)
            sheet.paylst.remove(t)


    
    def updatesheet(self,d): #update monthly balancesheet
        
        self.updatereceivable(d)
        self.updatepayable(d)
        self.updatebal()
        
        

    
    def updatebal(self):#updates balances in all tbalancesheets
        t=self.tlist[0]
        self.totpayable=0
        self.totreceivable=0
        if(isinstance(t,tbalancesheet)):
           t.updatebal()
           fin=t.finalbalance
           self.totpayable=self.totpayable+t.totpayable
           self.totreceivable=self.totreceivable+t.totreceivable
    

        for i in range(1,self.days,1):
    
            t=self.tlist[i]
            if(isinstance(t,tbalancesheet)):
                t.inibal=fin
                t.updateinibal()
                t.updatebal()
                fin=t.finalbalance
                self.totpayable=t.totpayable+self.totpayable
                self.totreceivable=t.totreceivable+self.totreceivable

    
    def updatereceivable(self,d):#update receivable
        sheet=self.tlist[d]
        if(len(sheet.recvlst)>0):
            for i in sheet.recvlst:
                
                if(isinstance(i,NotesTransaactiondate)):
                    if(len(i.amt.get())>0 and len(i.des.get())>0):
                        try:
                            a=int(i.amt.get()) #checks the amount is valid or not
                        except Exception as e:
                            messagebox.showerror('error','Invalid amount in receivable section in date '+str(i.cur))
                            return
                        if(i.ind in self.comrecvlst):
                            
                            translst=self.comrecvlst[i.ind]
                            translst[0].opentrans.des.config(state=NORMAL)
                            translst[0].opentrans.amt.config(state=NORMAL)
                            translst[0].opentrans.loadinfo(translst[0].des.get(),translst[0].amt.get())
                            translst[0].opentrans.des.config(state=DISABLED)
                            translst[0].opentrans.amt.config(state=DISABLED)
                
                        
                            if(len(translst)>1):
                                if(translst[0].amt.get()!=translst[1].amt.get() or translst[0].des.get()!=translst[1].des.get()): #checks the transaction is changed or not
                                
                                    for k in range(1,len(translst),1):
                                        if(isinstance(translst[k],NotesTransaactiondate)):
                                            
                                            translst[k].amt.config(state=NORMAL)
                                            translst[k].des.config(state=NORMAL)
                                            translst[k].loadinfo(translst[0].des.get(),translst[0].amt.get(),translst[0].status)
                                            translst[k].amt.config(state=DISABLED)
                                            translst[k].des.config(state=DISABLED)
                        else:
                            lst=[]
                            lst.append(i)
                            if(isinstance(sheet,tbalancesheet)):
                                opentran=sheet.odebit.addtransdetails(i.des.get(),i.amt.get())
                                opentran.amt.config(state=DISABLED)
                                opentran.des.config(state=DISABLED)
                                opentran.dele.config(state=DISABLED)
                                i.opentrans=opentran
                            for j in range(i.cur,self.days,1):
                                t=self.tlist[j]
                                if(isinstance(t,tbalancesheet)):
                                    trans=t.receivable.addtransdetails(i.des.get(),i.amt.get(),0,i.opendate,i.ind)
                                    trans.opentrans=opentran
                            
                                    trans.amt.config(state=DISABLED)
                                    trans.des.config(state=DISABLED)
                                    trans.dele.config(state=DISABLED)
                                    lst.append(trans)
                            self.comrecvlst[i.ind]=lst #stores list of all receivable transactions belongs to a single transaction in unique index 
                    else:
                        messagebox.showerror('Error','Invalid description and amount in receivable section in date'+str(i.cur))
                        return
                        
            
    
        if(len(sheet.finrecvlst)>0):
        #updates the status changed transactions
            n=len(sheet.finrecvlst)
            for i in range(0,n,1):
                t=sheet.finrecvlst[i]
                
            
                
                if(isinstance(t,NotesTransaactiondate)):
                    if(t.status==1):
                        closedate=t.closedate
                        sheet=self.tlist[t.closedate-1]
                        if(isinstance(sheet,tbalancesheet)):
                            close=sheet.ocredit.addtransdetails(t.des.get(),t.amt.get())
                            close.amt.config(state=DISABLED)
                            close.des.config(state=DISABLED)
                            close.dele.config(state=DISABLED)
                            t.closetrans=close
                            t.updatecloselab()
                            if(t.cur!=closedate):
                                t.status=0
                            lst=self.comrecvlst[t.ind]
                            for trans in lst:
                                if(isinstance(trans,NotesTransaactiondate)):
                                    if(t.closedate!=trans.cur):
                                        if(trans.cur<closedate):
                                            trans.statuschange()
                                            trans.closetrans=close
                                            trans.closedate=closedate
                                            trans.updatecloselab()
                                            trans.statusbut.config(state=DISABLED)
                                        else:
                                            trans.transfra.pack_forget()
                                            sec=self.tlist[trans.cur-1]
                            
                                            if(isinstance(sec,tbalancesheet)):
                                                sec.receivable.translst.remove(trans)


                                    else:
                                        if(trans.status==0):
                                            trans.statuschange()
                                        trans.closetrans=close
                                        trans.closedate=closedate
                                        trans.updatecloselab()
                       
                    else:
                        if(isinstance(t.closetrans,Transaction)):
                            t.closetrans.dele.config(state=NORMAL)
                            t.closetrans.dele.invoke()
                            t.closetrans=0
                            t.closedate=0
                            t.closelab.config(text='-')
                            lst=self.comrecvlst[t.ind]
                            for trans in lst:
                                if(isinstance(trans,NotesTransaactiondate)):
                                    if(t.cur!=trans.cur):
                                        if(trans.cur<t.cur):
                                            trans.closetrans=0
                                           
                                            trans.closelab.config(text='-')
                                            trans.statuschange()
                                            trans.closedate=0
                                            trans.statusbut.config(state=NORMAL)
                                        else:
                                            trans.transfra.pack()
                                            sec=self.tlist[trans.cur-1]
                                            if(isinstance(sec,tbalancesheet)):
                                                sec.receivable.translst.append(trans)
            
            while len(sheet.finrecvlst)>0: #deleting the updated transaction list
                del sheet.finrecvlst[0]

    def updatepayable(self,d): #update payable
        sheet=self.tlist[d]

        if(len(sheet.paylst)>0):
            for i in sheet.paylst:
                
                
                if(isinstance(i,NotesTransaactiondate)):
                    if(len(i.amt.get())>0 and len(i.des.get())>0):
                        try:
                            a=int(i.amt.get())
                        except Exception as e:
                            messagebox.showerror('error','Invalid amount in payable section in date'+str(i.cur))
                            return
                        if(i.ind in self.compaylst):
                            
                            translst=self.compaylst[i.ind]
                            translst[0].opentrans.des.config(state=NORMAL)
                            translst[0].opentrans.amt.config(state=NORMAL)
                            translst[0].opentrans.loadinfo(translst[0].des.get(),translst[0].amt.get())
                            translst[0].opentrans.des.config(state=DISABLED)
                            translst[0].opentrans.amt.config(state=DISABLED)
                            if(len(translst)>1):
                                if(translst[0].amt.get()!=translst[1].amt.get() or translst[0].des.get()!=translst[1].des.get()):
                                
                                    for k in range(1,len(translst),1):
                                        if(isinstance(translst[k],NotesTransaactiondate)):
                                            
                                            translst[k].amt.config(state=NORMAL)
                                            translst[k].des.config(state=NORMAL)
                                            translst[k].loadinfo(translst[0].des.get(),translst[0].amt.get(),translst[0].status)
                                            translst[k].amt.config(state=DISABLED)
                                            translst[k].des.config(state=DISABLED)
                        else:
                            lst=[]
                            lst.append(i)
                        
                            sheet=self.tlist[i.cur-1]
                            if(isinstance(sheet,tbalancesheet)):
                                opentran=sheet.ocredit.addtransdetails(i.des.get(),i.amt.get())
                                opentran.amt.config(state=DISABLED)
                                opentran.des.config(state=DISABLED)
                                opentran.dele.config(state=DISABLED)
                                i.opentrans=opentran
                            for j in range(i.cur,self.days,1):
                                t=self.tlist[j]
                                if(isinstance(t,tbalancesheet)):
                                    trans=t.payable.addtransdetails(i.des.get(),i.amt.get(),0,i.opendate,i.ind)
                                    trans.opentrans=opentran
                            
                                    trans.amt.config(state=DISABLED)
                                    trans.des.config(state=DISABLED)
                                    trans.dele.config(state=DISABLED)
                                    lst.append(trans)
                            self.compaylst[i.ind]=lst
                    else:
                        messagebox.showerror('Error','Invalid description and amount in payable section in date'+str(i.cur))
                        return
    
        if(len(sheet.finpaylst)>0):
            n=len(sheet.finpaylst)
        
            for i in range(0,n,1):
                t=sheet.finpaylst[i]
                if(isinstance(t,NotesTransaactiondate)):
                    if(t.status==1):
                        closedate=int(t.closedate)
                    
                        sheet=self.tlist[closedate-1]
                        if(isinstance(sheet,tbalancesheet)):
                            close=sheet.odebit.addtransdetails(t.des.get(),t.amt.get())
                            close.amt.config(state=DISABLED)
                            close.des.config(state=DISABLED)
                            close.dele.config(state=DISABLED)
                            t.closetrans=close
                            t.updatecloselab()
                            if(t.cur!=t.closedate):
                                t.status=0
                            lst=self.compaylst[t.ind]
                            for trans in lst:
                                if(isinstance(trans,NotesTransaactiondate)):
                                    if(closedate!=trans.cur):
                                        if(trans.cur<closedate):
                                            trans.statuschange()
                                            trans.closetrans=close
                                            trans.closedate=closedate
                                           
                                            trans.updatecloselab()
                                            
                                            trans.statusbut.config(state=DISABLED)
                                        else:
                                            trans.transfra.pack_forget()
                                            sec=self.tlist[trans.cur-1]
                                            if(isinstance(sec,tbalancesheet)):
                                                sec.payable.translst.remove(trans)

                                    else:
                                        if(trans.status==0):
                                            trans.statuschange()
                                        trans.closetrans=close
                                        trans.closedate=closedate
                                        trans.updatecloselab()
                       
                    else:
                        if(isinstance(t.closetrans,Transaction)):
                            t.closetrans.dele.config(state=NORMAL)
                            t.closetrans.dele.invoke()
                            t.closetrans=0
                            t.closedate=0
                            t.closelab.config(text='-')
                            lst=self.compaylst[t.ind]
                            for trans in lst:
                                if(isinstance(trans,NotesTransaactiondate)):
                                    if(t.cur!=trans.cur):
                                        if(trans.cur<t.cur):
                                            trans.closetrans=0
                                           
                                            trans.closelab.config(text='-')
                                            trans.statuschange()
                                            trans.closedate=0
                                            trans.statusbut.config(state=NORMAL)
                                        else:
                                            trans.transfra.pack()
                                            sec=self.tlist[trans.cur-1]
                                            if(isinstance(sec,tbalancesheet)):
                                                sec.payable.translst.append(trans)
            
            while len(sheet.finpaylst)>0:
                del sheet.finpaylst[0]
    def save(self,filename,win): #saves the informations as dictionary in a pickle file
        try:
            win.destroy()
            s=filename+'.pickle'
            path=os.getcwd()
            p=os.path.join(path,str(s))
            self.updatesheet(self.curdate-1)
            
            tiledetail={}
            tiledetail['cate']='balancetile'
            tiledetail['day']=self.days
            tiledetail['inibal']=self.ini
            tiledetail['monthnum']=self.mn
            tiledetail['year']=self.y
            tiledetail['month']=self.m
            paysheetlst=[]
            recvsheetlst=[]
            
            for i in range(0,self.days,1):
                balsheet=self.tlist[i]
                paylst=[]
                for t in balsheet.paylst:
                    transdic={}
                    if(isinstance(t,NotesTransaactiondate)):
                        if(len(t.des.get())>0 and len(t.amt.get())>0):
                            transdic['des']=t.des.get()
                            transdic['amt']=t.amt.get()
                            transdic['open']=t.opendate
                            transdic['stat']=t.status
                            
                            if(t.status==1):
                                transdic['close']=t.closedate
                                print('close ',t.closedate)
                            
                            else:
                                transdic['close']=0
                    
                            paylst.append(transdic)
                paysheetlst.append(paylst)
                recvlst=[]
                for t in balsheet.recvlst:
                    transdic={}
                
                    if(isinstance(t,NotesTransaactiondate)):
                        
                        if(len(t.des.get())>0 and len(t.amt.get())>0):
                            transdic['des']=t.des.get()
                            transdic['amt']=t.amt.get()
                            transdic['open']=t.opendate
                            transdic['stat']=t.status
                            if(t.status==1):
                                transdic['close']=t.closedate
                            

                            else:
                                transdic['close']=0
                            
                            recvlst.append(transdic)
                recvsheetlst.append(recvlst)

            tiledetail['receivable']=recvsheetlst
            tiledetail['payable']=paysheetlst
            sheetlst=[]
            
            for sheet in self.tlist:
                sheetdetail={}
                for sec in sheet.seclst:
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
                        sheetdetail[sec.title]=lst
                sheetlst.append(sheetdetail)

            tiledetail['sheetlst']=sheetlst
            fin=open(p,'wb+') 
            pkl.dump(tiledetail,fin)
            fin.close()
            for i in range(0,self.days,1):
                self.updatepayable(i)
                self.updatereceivable(i)
            self.updatebal()
            messagebox.showinfo('Info','Saved successfully')
            return filename
            
        except Exception as e:
            messagebox.showerror('error',str(e))
    
    def loadpkl(self,tiledetail): #load information from pickle and converts in to required format
        lst=[]
        if('payable' in tiledetail and 'receivable' in tiledetail ):
            sheetpaylst=tiledetail['payable']
            sheetrecvlst=tiledetail['receivable']
            n=len(sheetpaylst)
            for i in range(0,n,1):
                paylst=sheetpaylst[i]
                for t in paylst:
                    o=t['open']
                    c=t['close']
                    des=t['des']
                    amt=t['amt']
                    stat=t['stat']
                    trans=self.addnewpayable(self.tlist[o-1])
                    trans.loadinfo(des,amt,0)
                    trans.cur=o
                    trans.opendate=o
                    trans.status=stat
                    trans.closedate=c
                    trans.updateopenlab()
                    if(stat==1):
                        self.tlist[c-1].finpaylst.append(trans)
        
            
                recvlst=sheetrecvlst[i]
                for t in recvlst:
                    o=t['open']
                    c=t['close']
                    des=t['des']
                    amt=t['amt']
                    stat=t['stat']
                    trans=self.addnewreceivable(self.tlist[o-1])
                    trans.loadinfo(des,amt,0)
                    trans.cur=o
                    trans.opendate=o
                    trans.status=stat
                    trans.closedate=c
                    trans.updateopenlab()
                    if(stat==1):
                        self.tlist[c-1].finrecvlst.append(trans)
        if('sheetlst' in tiledetail):
            sheetlst=tiledetail['sheetlst']
            for i in range(0,self.days,1):
                sheetdetail=sheetlst[i]
                sheet=self.tlist[i]
                if(isinstance(sheet,tbalancesheet)):
                    for sec in sheet.seclst:
                        if(isinstance(sec,Section)):
                            lst=sheetdetail[sec.title]
                            for t in lst:
                                sec.addtransdetails(t['des'],t['amt'])
        for i in range(0,self.days,1):
            self.updatepayable(i)
            self.updatereceivable(i)
        self.updatebal()
        messagebox.showinfo('info','Loaded successfully')
    def disbargraph(self): #displays income and expense graph
        inc=[]
        exp=[]
        day=[]
        for i in range(0,self.days,1):
            day.append(i+1)
            inc.append(self.tlist[i].income.total)
            exp.append(self.tlist[i].expense.total)
        color=['green','red']

        
        n=numpy.arange(len(day))
        plt.bar(n+1-0.2,inc,0.4,color=color[0],label='Income')
        plt.bar(n+1+0.2,exp,0.4,color=color[1],label='Expense')
        plt.xticks(day)
        plt.xlabel='Date'
        plt.ylabel='Amount'
        plt.title('Income and expense graph')
        plt.legend()
        plt.show()
    
    def disrecvpiechart(self,translst): #displays receivable pie chart
        if(self.totreceivable!=0):
            def pcttoval(pct):
                val=int((pct*self.totreceivable)/100 + 0.5)
                if(val<100):
                    return ('%.2f%%  \n (%.2f )')%(pct,val)
                elif val >=100 and val <1000:
                    return ('%.2f%% \n (%.2f h )')%(pct,val/100)
                elif val>=1000 and val <10000:
                    return ('%.2f%% \n (%.2f k ))')%(pct,val/1000)
                else:
                    return ('%.2f%%  \n (%.2f l )')%(pct,val/100000)
            
            nrecv=0
            nrecvlab=['_received']
            nrecvval=[]
            explodelst=[0.1]

            for t in translst:
                if(isinstance(t,NotesTransaactiondate)):
                    if(t.status==0):
                        nrecv=nrecv+int(t.amt.get())
                        nrecvlab.append(t.des.get())
                        nrecvval.append(int(t.amt.get()))
                        explodelst.append(0)
                
            outcolor=['green','red']
            recv=self.totreceivable-nrecv
            outerlst=[recv,nrecv]
            outlab=['Received','Not received']
            inexplst=[0.1,0]
            innerlst=[recv]
            innerlst.extend(nrecvval)
            if(recv ==0 or nrecv==0):
                if(nrecv==0):
                    outerlst.remove(nrecv)
                    outcolor.remove('red')
                    innerlst=[recv]
                    del outlab[1]
                    del inexplst[1]
                elif recv==0:
                    outerlst.remove(recv)
                    outcolor.remove('green')
                    innerlst.remove(recv)
                    del nrecvlab[0]
                    del outlab[0]
                    del inexplst[0]
                    del explodelst[0]
            print(innerlst,outerlst,nrecvlab,outlab,outcolor,inexplst,explodelst)


            plt.pie(outerlst,colors=outcolor,radius=1,labels=outlab,startangle=90,wedgeprops={'linewidth':1.2,'edgecolor':'white'},explode=inexplst)
            wedge,texts,wre=plt.pie(innerlst,radius=0.7,labels=nrecvlab,startangle=90,wedgeprops={'linewidth':1.2,'edgecolor':'white'},autopct=lambda p:pcttoval(p),explode=explodelst)
            if(recv>0):
                wedge[0].set_facecolor('green')
                texts[0].set_visible(False)
            plt.title('Pie chart of receivables')
            plt.legend(loc=1)
            plt.show()
        else:
            messagebox.showinfo('Info','No transaction in receivable section')
    def dispaypiechart(self,translst): #displays payable pie chart
        if(self.totpayable!=0):
            def pcttoval(pct):
                val=int((pct*self.totpayable)/100 + 0.5)
                if(val<100):
                    return ('%.2f%%  \n (%.2f )')%(pct,val)
                elif val >=100 and val <1000:
                    return ('%.2f%% \n (%.2f h )')%(pct,val/100)
                elif val>=1000 and val <10000:
                    return ('%.2f%% \n (%.2f k ))')%(pct,val/1000)
                else:
                    return ('%.2f%%  \n (%.2f l )')%(pct,val/100000)
            
            npay=0
            npaylab=['_paid']
            npayval=[]
            explodelst=[0.1]

            for t in translst:
                if(isinstance(t,NotesTransaactiondate)):
                    if(t.status==0):
                        npay=npay+int(t.amt.get())
                        npaylab.append(t.des.get())
                        npayval.append(int(t.amt.get()))
                        explodelst.append(0)
                
            outcolor=['green','red']
            pay=self.totpayable-npay
            outerlst=[pay,npay]
            outlab=['Paid','Not Paid']
            inexplst=[0.1,0]
            innerlst=[pay]
            innerlst.extend(npayval)
            if(pay ==0 or npay==0):
                if(npay==0):
                    outerlst.remove(npay)
                    outcolor.remove('red')
                    innerlst=[pay]
                    del outlab[1]
                    del inexplst[1]
                elif pay==0:
                    outerlst.remove(pay)
                    outcolor.remove('green')
                    innerlst.remove(pay)
                    del npaylab[0]
                    del outlab[0]
                    del inexplst[0]
                    del explodelst[0]
            print(innerlst,outerlst,npaylab,outlab,outcolor,inexplst,explodelst)


            plt.pie(outerlst,colors=outcolor,radius=1,labels=outlab,startangle=90,wedgeprops={'linewidth':1.2,'edgecolor':'white'},explode=inexplst)
            wedge,texts,wre=plt.pie(innerlst,radius=0.7,labels=npaylab,startangle=90,wedgeprops={'linewidth':1.2,'edgecolor':'white'},autopct=lambda p:pcttoval(p),explode=explodelst)
            if(pay>0):
                wedge[0].set_facecolor('green')
                texts[0].set_visible(False)
            plt.title('Pie chart of Payable')
            plt.legend(loc=1)
            plt.show()
        else:
            messagebox.showinfo('Info','No transaction in payable section')
            
        
        
def makecenter(p,sw,sh,pw,ph):

    w=(sw-pw)/2
    w=int(w)
    h=(sh-ph)/2
    h=int(h)
    p.geometry(('%dx%d+%d+%d')%(pw,ph,w,h))


class warningbox: #warning box to inform current data will be deleted
    def __init__(self,parent):
        self.curtitle=curtile
        self.win=Toplevel(root)
        self.win.geometry('300x60')
        self.win.title='Warning'
        warlab=Label(self.win,text='The current data will be deleted.')
        warlab.pack(side='top',anchor=CENTER)
        self.okbut=Button(self.win,text='Ok',width=10)
        self.cancelbut=Button(self.win,text='Cancel',width=10)
        self.okbut.pack(side='left',padx=20)
        self.cancelbut.pack(side='right',padx=20)
        makecenter(self.win,sw,sh,300,60)

        self.cancelbut.config(command=self.win.destroy)
        
    
    

def delecurtile():
    global curtile
    if( curtile!=0):
        if(isinstance(curtile,balancetile)):
            curtile.sheetfra.destroy()
            curtile=0
        if(isinstance(curtile,eventtile)):
            curtile.evenfra.destroy()
            curtile=0
    

        
    

def selectpklfile(): #to select required files from computer
    
    p=os.getcwd()
    f=filedialog.askopenfilename(initialdir=p)
    w=warningbox(root)
   
    def openpkl():
        try:
            global curtile,curfilename
            w.win.destroy()
            delecurtile()
            fin=open(f,'rb')
            basename=os.path.basename(f)
            name=os.path.splitext(basename)
            curfilename=name[0]
            tiledetail=pkl.load(fin)
            fin.close()
            if(isinstance(tiledetail,dict)):
                if('cate' in tiledetail):#checcks it belongs to this program
                    if(tiledetail['cate']=='eventtile'):  #checks if it belongs to event balancesheet
                        keylst=list(tiledetail.keys())
                        if('date' in tiledetail and 'inibal' in tiledetail):
                            curtile=eventtile(root,tiledetail['name'],tiledetail['date'],tiledetail['inibal'],sw,sdic)
                            curtile.loadpkl(tiledetail)
                    elif tiledetail['cate']=='balancetile': #checks if it belongs to monthly balanacesheet
                        if('day' in tiledetail and 'inibal' in tiledetail and 'monthnum' in tiledetail and 'year' in tiledetail and 'month' in tiledetail):
                            curtile=balancetile(root,tiledetail['day'],tiledetail['month'],tiledetail['year'],tiledetail['inibal'],tiledetail['monthnum'])
                            curtile.loadpkl(tiledetail)
                else:
                    messagebox.showerror('Invalid pickle file','Select a pickle file belongs to this program')
            else:
                messagebox.showerror('Invalid pickle file','Select a pickle file belongs to this program')
        except Exception as e:
            messagebox.showerror('Error',str(e))
    w.okbut.config(command=openpkl)
    if(curtile==0):
        w.okbut.invoke()

    
            
            
def checkint(s):
    try:
        int(s)   
    except ValueError:
        return False
    else:
        return True



def getdetailsfornewevent(): #gets details for new event
    eventwin=Toplevel(root)
    eventwin.geometry('300x110')
    eventwin.resizable(width=False,height=False)
    lname=Label(eventwin,text='enter the name of the event:')
    lname.grid(row=0,column=0,sticky=E)
    ename=Entry(eventwin)
    ename.grid(row=0,column=1)
    makecenter(eventwin,sw,sh,300,110)

    datelab=Label(eventwin,text='Select a date:')
    datelab.grid(row=1,column=0,sticky=E)

    cur=date.today()
    curs=date.today().strftime('%d- %m -%Y')
    datebut=Button(eventwin,text=curs,bd=0)
    datebut.grid(row=1,column=1)
    ballab=Label(eventwin,text='Enter the initial balance:')
    ballab.grid(row=2,column=0,sticky=E)
    ebal=Entry(eventwin)
    ebal.grid(row=2,column=1)
    okbut=Button(eventwin,text='Ok',width=10)
    okbut.grid(row=3,column=0,padx=20,pady=10)
    cancelbut=Button(eventwin,text='Cancel',command=eventwin.destroy,width=10)
    cancelbut.grid(row=3,column=1,padx=20,pady=10)

    def getdatecal(): #create calendar to select date
        calwin=Toplevel(eventwin)
        datebut.config(state=DISABLED)
        calwin.protocol("WM_DELETE_WINDOW", DISABLED)
       
        cal=Calendar(calwin,selectmode='day',day=cur.day,year=cur.year,month=cur.month,date_pattern='dd-MM-yyyy')
        cal.pack()
        cw=calwin.winfo_reqwidth()
        ch=calwin.winfo_reqheight()
        makecenter(calwin,sw,sh,cw,ch)
        def selecdate(event):
            date=cal.get_date()
        
        
            datebut.config(state=NORMAL)
            datebut.config(text=date)
            calwin.destroy()
        cal.bind('<<CalendarSelected>>',selecdate)
    datebut.config(command=getdatecal)
    def createevent(): #creates a new event balancesheet with information collection and also checks for any errors
        try:
            if(len(ename.get())==0):
                messagebox.showerror('Warning','Enter a valid event name')
                eventwin.destroy()
                return
            eventname=ename.get()
            eventbal=ebal.get()
            if(checkint(eventbal)==False):
                  messagebox.showerror('Warning','Enter a valid initial balance')
                  eventwin.destroy()
                  return
            eventwin.destroy()
            
            w=warningbox(root) #displays warning box
            
            def okbutonclick():
                global curtile,curfilename
                w.win.destroy()
                delecurtile()
                curfilename=''
                t=eventtile(root,eventname,str(cur),int(eventbal),sw,sdic)
                curtile=t
            w.okbut.config(command=okbutonclick)
            if(len(curfilename)==0):
                w.okbut.invoke()
            
        except Exception as e:
            print(e)
    okbut.config(command=createevent)
            

def createbalancesheet(m,y,balentr,monthlst,win): #creates a new monthly balancesheet with information collection and also checks for any errors
    try:
        bal=int(balentr.get())
        y=int(y)
        win.destroy()
        days=0
        if(isinstance(monthlst,list)):
            monthnum=monthlst.index(m)+1
        if(monthnum==2):
            if(y%4==0):
                if y%100==0:
                    if y%400==0:
                        days=29
                    else:
                        days=28
                else:
                    days=29
            else:
                days=28
        elif monthnum%2==0:
            days=30
        else:
            days=31
        w=warningbox(root) #displays warning box
        global curtile
        
        
        def okbutonclick():
            global curfilename
            curfilename=''
            w.win.destroy()
            delecurtile()
            global curtile
            t=balancetile(root,days,m,y,int(bal),monthnum)
            curtile=t
        w.okbut.config(command=okbutonclick)
        if(curtile==0):
            w.okbut.invoke()
    except Exception as e:
        messagebox.showerror('Invalid balance','Enter a valid initial balance')
        balentr.delete(0,END)
        win.destroy()
        return
            

def getfilename(): #get file name to store the file from user
    savewin=Toplevel(root)
    savewin.geometry('300x60')
    makecenter(savewin,sw,sh,300,60)
    namefra=Frame(savewin)
    filelab=Label(namefra,text='Enter the filename to save:')
    filelab.pack(side='left')
    fileen=Entry(namefra)
    fileen.pack(side='left')
    namefra.pack(side='top',anchor='center')
    sbut=Button(savewin,text="Save",width=10)
    def savebutonclick():
        global curfilename
        if(isinstance(curtile,eventtile) or isinstance(curtile,balancetile)):
            if(len(fileen.get())>0):
                curfilename=curtile.save(fileen.get(),savewin)
                
            else:
                messagebox.showerror('Invalid file name','enter a valid file name to save')
        else:
            messagebox.showinfo('Info','No data to save')
    sbut.config(command=savebutonclick)
    sbut.pack(side='left',padx=20)
    cbut=Button(savewin,text='Cancel',command=savewin.destroy,width=10)
    cbut.pack(side='right',padx=20)
           

def checkfile(): #check the during saving for overriding or not
    if(len(curfilename)==0):
        getfilename()
    else:
        win=Toplevel(root)
        win.geometry('300x60')
        win.title='Info'
        warlab=Label(win,text='Do you want to overwrite the file')
        warlab.pack(side='top',anchor=CENTER)
        okbut=Button(win,text='Yes',width=10)
        def overwrite():
            if(isinstance(curtile,eventtile) or isinstance(curtile,balancetile)):
                curtile.save(curfilename,win)
        okbut.config(command=overwrite)
        def newfile():
            getfilename()
                  
        cancelbut=Button(win,text='No',width=10,command=newfile)
        
        okbut.pack(side='right',padx=20)
        cancelbut.pack(side='left',padx=20)
        makecenter(win,sw,sh,300,60)
        

def getdetailforbalancesheet(): #get details for monthly balancesheet from user
    monthlst=['January','February','March','April','May','June','July','August','September','October','November','December']
    yearlst=[]
    for  i in range(2023,2041,1):
        yearlst.append(i)
    monthvar=Variable(value=monthlst)
    yearvar=Variable( value=yearlst)
    sheetwin=Toplevel(root)
    cur=date.today()
    dat={}
    dat['m']=monthlst[int(cur.month)-1]
    dat['y']=cur.year
    def createlistbox(selbut,sel,lst):
        lstvar=Variable(value=lst)
        lstwin=Toplevel(root)
        lstwin.protocol("WM_DELETE_WINDOW", DISABLED)
        if(isinstance(selbut,Button)):
            selbut.config(state=DISABLED)
        lstbox=Listbox(lstwin,selectmode=SINGLE,listvariable=lstvar)
        lstbox.pack()
        lw=lstbox.winfo_reqwidth()
        lh=lstbox.winfo_reqheight()
        makecenter(lstwin,sw,sh,lw,lh)
        def updateall(event):
            i=lstbox.curselection()[0]
        
            
            dat[sel]=lst[i]
            selbut.config(text=lst[i])
            lstwin.destroy()
            selbut.config(state=NORMAL)


        lstbox.bind('<<ListboxSelect>>',updateall)

        
    sheetwin.geometry('300x120')
    makecenter(sheetwin,sw,sh,300,120)
    monthlab=Label(sheetwin,text='Select a month:')
    monthlab.grid(row=0,column=0,sticky=E)
    monthbut=Button(sheetwin,text=dat['m'],command=lambda:createlistbox(monthbut,'m',monthlst),bd=0)
    monthbut.grid(row=0,column=1)

    yearlab=Label(sheetwin,text='Select a year:')
    yearlab.grid(row=1,column=0,sticky=E)
    yearbut=Button(sheetwin,text=dat['y'],command=lambda:createlistbox(yearbut,'y',yearlst),bd=0)
   
    yearbut.grid(row=1,column=1)
    ballab=Label(sheetwin,text='Enter the initial balance:')
    ballab.grid(row=2,column=0,sticky=E)
    balentr=Entry(sheetwin)
    balentr.grid(row=2,column=1)
   
    
    okbut=Button(sheetwin,text='Ok',width=10,command=lambda:createbalancesheet(dat['m'],dat['y'],balentr,monthlst,sheetwin,))
    okbut.grid(row=3,column=0,padx=20,pady=10)
    cancelbut=Button(sheetwin,text='Cancel',width=10,command=sheetwin.destroy)
    cancelbut.grid(row=3,column=1,padx=20,pady=10)



root=Tk()
root.title('FinNoter') #assigning title
icon=ImageTk.PhotoImage(Image.open(r'./Assets/pyicon.jpg'))#loading icon
root.iconphoto(True,icon)

global sdic,sh,curfilename
sh=root.winfo_screenheight() #load screen height
sw=root.winfo_screenwidth() #load screen width
curfilename=''
tr=Transaction(root,sw) 
ntr=NotesTransaction(root,sw) #crearting all types of transaction to get required width
ndtr=NotesTransaactiondate(root,0,0,0,sw,0,0) #

root.update_idletasks()

root.geometry(f'{sw}x{sh}+0+0')
sdic={}
sdic['transwid']=tr.transfra.winfo_reqwidth() #getting rrequired width of all transaction and storing it as dictionary
sdic['transdes']=tr.des.winfo_reqwidth()
sdic['notewid']=ntr.transfra.winfo_reqwidth()
sdic['ndatewid']=ndtr.transfra.winfo_reqwidth()
sdic['notedes']=ntr.des.winfo_reqwidth()
sdic['ndatedes']=ndtr.des.winfo_reqwidth()
sdic['ndateclose']=ndtr.openlab.winfo_reqwidth()
root.update_idletasks()
tr.transfra.destroy()
ntr.transfra.destroy()#deleting the created transactions
ndtr.transfra.destroy()

path=os.getcwd()
d="FinNoter" #creating directory for application to store data
p=os.path.join(str(path),d)
if(os.path.isdir(p)):
    os.chdir(p)
    pass
else:
    os.mkdir(p,0o666)
    os.chdir(p)


root.configure(background='SlateGray2')
menubar=Menu(root,bg='SlateGray2',fg='SlateGray2')
options=Menu(menubar,tearoff=0)
menubar.add_cascade(label='options',menu=options)
options.add_command(label='New month balancesheet',command=getdetailforbalancesheet)
options.add_command(label='New event balancesheet',command=getdetailsfornewevent)
options.add_command(label='Open',command=lambda:selectpklfile())
options.add_command(label='Save',command=checkfile)
options.add_separator()
options.add_command(label='Exit', command=root.destroy)
root.config(menu=menubar)

root.mainloop()
 