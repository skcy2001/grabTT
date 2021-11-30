import tkinter as tk
from tkinter import *
import json
from functools import partial

def allotslotstxt(slots,file):
    allots = {}
    lines = open(file,'r').readlines()
    subj = []
    for line in lines:
        if line == "\n":
            allots[subj[0]] = subj[1:]
            subj = []
        else:
            subj.append(line[:-1])
    
    allotslotsgui(slots,allots=allots)
    return allots

def allotslotsgui(slots,allots = {}):

    def refresh(tab,label):

        nonlocal slots, allots

        for row in tab:
            for cell in row:
                    for slot in cell:
                        cell[slot]['background'] = '#EEEEEE'
                        cell[slot]['foreground'] = '#000000'
        finalbusy = []
        for main in allots:
            tempbusy = []
            for coord in slots[main]:
                for slotts in tab[coord[0]][coord[1]]:
                    tempbusy.append(slotts)
            
            busy = list(set(tempbusy))
            finalbusy += busy

            for slott in busy:
                for coord in slots[slott]:
                    if tab[coord[0]][coord[1]][slott]['background'] == 'green':
                        tab[coord[0]][coord[1]][slott]['background'] = 'black'
                        tab[coord[0]][coord[1]][slott]['foreground'] = 'white'
                    else: tab[coord[0]][coord[1]][slott]['background'] = 'red'

            for coord in slots[main]:
                tab[coord[0]][coord[1]][main]['background'] = 'green'
        
        free = set()
        free = set(slots.keys()) - set(finalbusy)
        label['text'] = "Free slots: " + str(free).strip('{}')

    def register(tab,entry,label):
        nonlocal slots,allots

        tkn = [x.strip() for x in entry.get().split("|")]
        if len(tkn) > 0:
            slot = tkn[0]
        else: 
            refresh(tab,label)
            return
        if len(tkn) > 1:
            subj = tkn[1]
        else:
            del allots[slot]
            refresh(tab,label)
            return
        if len(tkn) > 2:
            code = tkn[2]
        else: code= ""
            
        allots[slot] = [subj,code]
        refresh(tab,label)
        entry.set("")

    l,b=5,9
    win = tk.Tk()

    win.title("Allot slots")
    win.geometry("900x400")
    win.rowconfigure(0,weight=7)
    win.rowconfigure(1,weight=1)
    win.columnconfigure(0,weight=1)
    
    table = tk.Frame(win)
    table.grid(row=0,column=0,padx=20,pady=20,sticky='nsew')
    mat = [[]]
    tab = [[]]
    
    for i in range(l):
        table.rowconfigure(i,weight=1)
    for i in range(b):
        table.columnconfigure(i,weight=1)
    
    for i in range(l):
        for j in range(b):
            tab[i].append({})
            mat[i].append(tk.Frame(table,relief=GROOVE,bd=5))
            mat[i][j].grid(row=i,column=j,sticky='nsew')
        mat.append([])
        tab.append([])

    for slot in slots:
        for coord in slots[slot]:
            tab[coord[0]][coord[1]][slot] = tk.Label(mat[coord[0]][coord[1]],text=slot,relief=GROOVE)
            tab[coord[0]][coord[1]][slot].pack(fill='both',expand=True, side=LEFT)

    footer = tk.Frame(win)
    footer.grid(row=1,column=0,padx=20,sticky='nsew')
    L1 = tk.Label(footer,text="")
    L1.pack(fill='x')
    entry = tk.StringVar(table)
    E1 = tk.Entry(footer,textvariable=entry).pack(side='left',fill='x',expand=True)
    B1 = tk.Button(footer,command = lambda : register(tab,entry,L1),text="Submit").pack(side='left')
    B2 = tk.Button(footer,command= lambda: win.destroy(), text = "Print").pack(side='left')
    refresh(tab,L1)

    win.mainloop()

    json.dump(allots,open('bin/allots.json','w'))
    return allots

def allotslotsmaster(tkn, slots):
    if tkn == "":
        allots = allotslotsgui(slots)
    else:
        if tkn[-4:] == 'json': 
            return json.load(open(tkn,"r"))
        allots = allotslotstxt(slots,tkn)
    
    return allots
