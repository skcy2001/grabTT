import sys
from time import sleep
import math
from driver import *
from tkinter.constants import LEFT, NSEW
from datetime import datetime
import tkinter as tk
from tkinter import Button, StringVar, font, Label
import json
import pandas as pd
import tkcap
   
def makeroutine(slots,allots):

    root = tk.Tk()
    root.title('Semester Routine')

    # Root Configuration
    root.geometry("1000x480")
    root.rowconfigure(0, weight=20)
    root.columnconfigure(0, weight=1)

    myc = TT_data()
    periods = myc.createPeriods(['8am', '6pm', '55m', '5m', '1pm', '1h'])  
    myt = TT_frame(periods, master=root)
    
    F = Frame(root)
    F.grid(row=1,column=0,sticky=NSEW)
    Label(F,text="5th Sem").pack(side=LEFT)
    Label(F,text="IIT Kharagpur ECE").pack(side=tk.RIGHT)
    Label(F,text="Samyak Chakrabarty").pack()
        
    table,events = slottott(slots,allots,myt,periods)
    table = pd.DataFrame(table)
    table.to_csv(open("tt.csv",'w'))
    caltoics(events)
    
    root.mainloop()
