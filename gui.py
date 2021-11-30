import tkinter as tk
from utilfunc.writeslots import *
from utilfunc.allotslots import *
import sys
from main import makeroutine

slots = {}
allots = {}

# STEP 1
app = tk.Tk()
app.geometry("300x100+100+100")
app.title("Timetable Creator IIT KGP")
app.columnconfigure(0,weight=1)

def submit1(S):
    global slots
    slots = writeslotsmaster(S)
    app.destroy()
    return slots

def reset1():
    S.set("")

L1 = tk.Label(app,text="Enter 'slots' file location:\n (leave empty to manually enter slot)")
L1.grid(row=0,column=0,padx=1,pady=1)
F = tk.Frame(app)
F.grid(row=1,column=0,padx=5,pady=5)

S = tk.StringVar()
S.set("bin/slots.json")
E1 = tk.Entry(F,textvariable=S,width=20).pack(side="left",padx=1,pady=1)
B1 = tk.Button(F, text = "Submit",command= lambda : submit1(S.get())).pack(side="left",padx=1,pady=1)
B2 = tk.Button(F, text = "Reset",command= reset1).pack(side="left",padx=1,pady=1)

app.mainloop()

if slots == {}:
    sys.exit()

#Step 2
app2 = tk.Tk()
app2.geometry("300x100+100+100")
app2.title("Timetable Creator IIT KGP")
app2.columnconfigure(0,weight=1)

def submit2(S):
    global allots, slots
    app2.destroy()
    allots = allotslotsmaster(S,slots)
    return allots

def reset2():
    S.set("")

L1 = tk.Label(app2,text="Enter 'allotments' file location:\n (leave empty to manually enter slot)")
L1.grid(row=0,column=0,padx=1,pady=1)
F = tk.Frame(app2)
F.grid(row=1,column=0,padx=5,pady=5)

S = tk.StringVar(F,"bin/allots.json")
E1 = tk.Entry(F,textvariable=S,width=20).pack(side="left",padx=1,pady=1)
B1 = tk.Button(F, text = "Submit",command= lambda : submit2(S.get())).pack(side="left",padx=1,pady=1)
B2 = tk.Button(F, text = "Reset",command= reset2).pack(side="left",padx=1,pady=1)

app2.mainloop()

makeroutine(slots,allots)

