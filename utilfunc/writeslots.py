import tkinter as tk
from tkinter import *
import json
from functools import partial

def writeslotsgui(dim):
    
    masterslots = []
    win = tk.Tk()
    slctstr = StringVar()
    slotn = StringVar()
    selected = []

    def filef():
        json.dump(masterslots,open("bin/slots.json","w"))
    
    def slotadd(x,y,matrix):
        nonlocal selected, slctstr
        matrix[x][y]['state'] = DISABLED
        matrix[x][y]['relief'] = SUNKEN
        selected.append((x,y))
        slctstr.set(json.dumps(selected))
        
    def saveslot():
        nonlocal mat, selected, slotn, masterslots, slctstr
        
        for slot in selected:
            mat[slot[0]][slot[1]]['state'] = NORMAL
            mat[slot[0]][slot[1]]['relief'] = RIDGE
            
        
        slotdict = {}
        slotdict[slotn.get()] = selected
        selected = []
        slctstr.set("")
        masterslots.append(slotdict)
    
    def resetf():
        nonlocal mat, selected, slctstr
        
        for slot in selected:
            mat[slot[0]][slot[1]]['state'] = NORMAL
            mat[slot[0]][slot[1]]['relief'] = RIDGE

        selected = []
        slctstr.set("")
        
    l,b=dim
    
    win.title("Create slots")
    win.geometry("900x400")
    win.rowconfigure(0,weight=7)
    win.rowconfigure(1,weight=1)
    win.columnconfigure(0,weight=1)
    
    table = tk.Frame(win)
    table.grid(row=0,column=0,padx=20,pady=20,sticky='nsew')
    mat = [[]]
    
    for i in range(l):
        table.rowconfigure(i,weight=1)
    for i in range(b):
        table.columnconfigure(i,weight=1)
    
    for i in range(l):
        for j in range(b):
            mat[i].append(tk.Button(table))
            mat[i][j]['text'] = str(i)+","+str(j)
            mat[i][j].grid(row=i,column=j,sticky='nsew')
            mat[i][j]['command'] = partial(slotadd,i,j,mat)
            mat[i][j]['relief'] = RIDGE
        mat.append([])
    
    footer = tk.Frame(win)
    footer.grid(row=1,column=0,padx=20,sticky='nsew')
    
    slots = tk.Entry(footer,state=DISABLED, textvariable=slctstr,width=10)
    slots.pack(fill='x',expand=True,side=LEFT,padx=1)
    slotname = tk.Entry(footer,textvariable=slotn,width=5)
    slotname.pack(side=LEFT,padx=1)
    save = tk.Button(footer, text='Save Slot', command= lambda : saveslot())
    save.pack(side=LEFT,padx=1)
    reset = tk.Button(footer, text='Reset', command= lambda : resetf())
    reset.pack(side=LEFT,padx=1)
    file = tk.Button(footer, text='Save File', command= lambda : filef())
    file.pack(side=LEFT,padx=1)
    win.mainloop()

    return(masterslots)

def writeslotstxt(file):
    with open(file,'r') as f:
        lines = f.readlines()
    
    slots = {} 
    x = []
    for line in lines:
        if line == '\n':
            slots[x[0]]=[[int(y) for y in xy.split(',')] for xy in x[1:]]
            x=[]
        else: x.append(line[:-1])
    
    json.dump(slots,open("bin/slots.json","w"))
    return slots

def printslots(slots):
    cout = ""
    for slot in slots.keys():
        cout += str(slot) + "\n"
        for xy in slots[slot]:
            cout += str((" -",xy[0],xy[1])) + "\n"
    
    return cout

def writeslotsmaster(tkn):
    if tkn == "":
        slots = writeslotsgui((5,9))
    else:
        if tkn[-4:] == 'json': 
            return json.load(open(tkn,"r"))
        slots = writeslotstxt(tkn)
    return slots