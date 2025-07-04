from tkinter import *
def percensize(p,w):
    s=int(w-13)/7
    s=s+1
    s=s/100
    s=s*p
    return int(s)
class Transaction: #creating class to manage single transaction
    def __init__(self,parent,sw):
        self.transfra=Frame(parent)
        self.des=Entry(self.transfra,width=percensize(5.5,sw))
        
        self.des.pack(side='left')
        self.amt=Entry(self.transfra,width=percensize(5.5,sw))

        
        self.amt.pack(side='left')
        self.dele=Button(self.transfra,text='x',bd=0,width=percensize(1.5,sw))

        self.dele.pack(side='left')
        
        self.transfra.pack(side='top')
    def loadinfo(self,des,amt): #used to load data from file
        self.des.delete(0,END)
        self.amt.delete(0,END)
        self.des.insert(0,des)
        self.amt.insert(0,str(amt))

class NotesTransaction: #class to manage single notetransaction in a event balancesheet

    def __init__(self,parent,sw):
        self.opentrans=0
        self.closetrans=0
        self.transfra=Frame(parent)
        self.status=0
        self.des=Entry(self.transfra,width=percensize(10.5,sw))
        self.des.pack(side='left')
        self.amt=Entry(self.transfra,width=percensize(10.5,sw))
        self.amt.pack(side='left')
        self.statusbut=Button(self.transfra,text='-',width=percensize(1.5,sw),bd=0)
        self.statusbut.pack(side='left')
        self.dele=Button(self.transfra,text='x',bd=0,width=percensize(1.5,sw))
        self.dele.pack(side='right')
        self.transfra.pack(side='top')
        def statuschange(): # used to  give function to status button
            if(self.status==0):
                self.status=1
                self.statusbut.config(text='🗸',bg='green')
            else:
                self.status=0
                self.statusbut.config(text='-',bg='red')

        self.statusbut.config(command=statuschange)
    def loadinfo(self,des,amt,status):
        self.des.delete(0,END)
        self.amt.delete(0,END)
        
        self.des.insert(0,des)
        self.amt.insert(0,str(amt))
        if(status==1):
            self.statusbut.invoke()
    
class NotesTransaactiondate: #class to manage single notetransaction in a month balancesheet
    def __init__(self,parent,open,m,y,sw,cur,ind):
        self.ind=ind
        self.opentrans=0
        self.closetrans=0
        self.opendate=open
        self.cur=cur
        self.monyear='/'+str(m)+'/'+str(y)
        self.closedate=0
        self.transfra=Frame(parent)
        self.status=0
        self.des=Entry(self.transfra,width=percensize(6.8,sw))
        self.des.pack(side='left')
        self.amt=Entry(self.transfra,width=percensize(6.8,sw))
        self.amt.pack(side='left')
        self.openlab=Label(self.transfra,text=str(self.opendate)+self.monyear,width=percensize(4,sw),font=('Arial',8))
        self.openlab.pack(side='left')
        self.closelab=Label(self.transfra,text='-',width=percensize(4,sw),font=('Arial',8))
        self.closelab.pack(side='left',anchor=W)
        self.statusbut=Button(self.transfra,text='-',width=percensize(1.5,sw),bd=0)
        self.statusbut.pack(side='left')
        self.dele=Button(self.transfra,text='x',bd=0,width=percensize(1.5,sw))
        self.dele.pack(side='right')
        self.transfra.pack(side='top')
      
    def updatecloselab(self): #updates the close date label
        self.closelab.config(text=str(self.closedate)+self.monyear)  
    def statuschange(self): # used to  give function to status button
        if(self.status==0):
            self.status=1
            self.closedate=self.cur
            self.statusbut.config(text='🗸',bg='green')
        else:
            self.closedate=0
            self.status=0
            self.statusbut.config(text='-',bg='red')
    def loadinfo(self,des,amt,status):
        self.des.delete(0,END)
        self.amt.delete(0,END)
        self.des.insert(0,des)
        self.amt.insert(0,str(amt))
        if(status==1):
            self.statusbut.invoke()
    def statusfun(self,lst): #
        print(len(lst))
        if(isinstance(self,NotesTransaactiondate)):
            if(self in lst):
                self.statuschange()
            else:
                self.statuschange()
                lst.append(self)
    def updateopenlab(self): #update the open date label
        self.openlab.config(text=str(self.opendate)+self.monyear) 

    
    
    
        
    

