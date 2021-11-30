from icalendar import Calendar, Event
import sys
import math
from datetime import datetime, timedelta
import re
import pandas as pd
import tkinter as tk
from tkinter import Button, Label, Frame
from tkinter.constants import NSEW
import tkcap
from utilfunc.miscf import *

def caltott(cal, tt):
    for event in cal.events:
        tt.drawPeriod(event['summary'], event['description'], (event['day'],
                      event['periods'][0]), colsp=len(event['periods']))

    for i in range(len(cal.table)):
        for j in range(len(cal.table[0])):
            k = 0
            while cal.table[i][j] == '':
                cal.table[i][j] = 'null'
                k += 1
            if k > 0:
                print((i, j), k)
                k = 0

def slottott(slots, alotts, tt,periods):
    table = [['', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', ''], ['', '', '', '',
                                                                                          '', '', '', '', ''], ['', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '']]
    events = []
    for alott in alotts:
        slot = slots[alott]
        for xy in slot:
            table[xy[0]][xy[1]] = (alotts[alott][0], alotts[alott][1])
            span = 1
            while [xy[0], xy[1]+span] in slot:
                table[xy[0]][xy[1]+span] = (alotts[alott][0], alotts[alott][1])
                slot.remove([xy[0], xy[1]+span])
                span += 1
            tt.drawPeriod(alotts[alott][0], alotts[alott][1], xy, span)
            start = list(periods.keys())[xy[1]]
            start = datetime(2021,8,16+xy[0],start.hour,start.minute)
            end = periods[list(periods.keys())[xy[1]+span-1]]
            end = datetime(2021,8,16+xy[0],end.hour,end.minute)
            events.append((alotts[alott][0], alotts[alott][1], start, end))
            
    for i in range(5):
        for j in range(9):
            k=0
            while table[i][j+k] == "":
                table[i][j+k] = " "
                k+=1
                if j+k > 8: break
            if k > 0: tt.drawPeriod("","",(i,j),k)

    return table,events

def caltoics(events):

    cal = Calendar()
    for item in events:
        event = Event()
        event.add("summary", item[0])
        event.add("dtstart", item[2])
        event.add("dtend", item[3])
        event.add("description", item[1])
        event.add("rrule", {"freq": "weekly"})
        cal.add_component(event)
        
    f = open("tt.ics", "wb")
    f.write(cal.to_ical())
    f.close()

class TT_data():
    def __init__(self):
        self.events = []
        self.periods = {}
        self.slots = {}
        self.table = [[], [], [], [], []]

    def createPeriods(self, tkn):
        '''
        Perioding - To create periods timing 
            input = list of variables:
                -start time:
                    time format supported by proj
                -end time:
                    time format supported by proj
                -duration:
                    '1h' = [dt.timedelta(hour=1)]
                    '[1h,,]' = [dt.timedelta(hour=1),dt.timedelta(hour=1),dt.timedelta(hour=1)]
                    '[30min(2),] = [dt.timedelta(minute=30),dt.timedelta(minute=30),dt.timedelta(minute=30)]
                -breaks:
                    same as duration
                -recess start time:
                    list of start times in time format supported by proj
                -recess duration:
                    list of recess durations in duration format supported by proj
            output = list of tuples:
                -each tuple:
                    -starttime = datetimeobj
                    -endtime = datetimeobj    
        '''
        start = extracttime(tkn[0])
        end = extracttime(tkn[1])
        periods = {}
        dur_temp = []
        duration = tkn[2].strip('[] ').split(',')
        for i, x in enumerate(duration):
            if x == '':
                dur_temp.append('')
                continue
            y = re.findall(r'(.+)\{([0-9]+)\}', x)
            if len(y) > 0:
                y = y[0]
            else:
                y = [x, 1]

            for ii in range(int(y[1])):
                dur_temp.append(y[0])

        for i, x in enumerate(dur_temp):
            if x == '':
                dur_temp[i] = dur_temp[i-1]
        duration = dur_temp

        brk_temp = []
        breaks = tkn[3].strip('[]').split(',')
        for i, x in enumerate(breaks):
            if x == '':
                brk_temp.append('')
                continue
            y = re.findall(r'(.+)\{([0-9]+)\}', x)
            if len(y) > 0:
                y = y[0]
            else:
                y = [x, 1]

            for ii in range(int(y[1])):
                brk_temp.append(y[0])

        for i, x in enumerate(brk_temp):
            if x == '':
                brk_temp[i] = brk_temp[i-1]
        breaks = brk_temp

        rec_temp = {}
        recesses = tkn[4].strip('[]').split(',')
        recessdurs = tkn[5].strip('[]').split(',')

        for i in range(len(recesses)):
            rec_temp[extracttime(recesses[i])] = extractduration(recessdurs[i])

        recess = rec_temp

        i = 0
        event_start = start
        while event_start < end:
            for time in duration:

                while event_start in recess.keys():
                    event_start += recess[event_start]

                event_dur = extractduration(time)
                event_end = event_start + event_dur

                if event_end > end:
                    continue

                periods[event_start] = event_end

                event_start += event_dur + extractduration(breaks[i])
                i = (i + 1) % len(breaks)

        # Testing printer
        #for period in periods: print(period.strftime("%H:%M") + ' - ' + periods[period].strftime("%H:%M"))

        self.periods = periods
        for i in range(5):
            for j in range(len(self.periods)):
                self.table[i].append("")

        return periods

    def addEvent(self, tkn):

        day, start, end, name, description = tkn

        day = extractday(day)
        start = extracttime(start)
        end = extracttime(end)

        period = []
        periodstarts = list(self.periods.keys())
        i = periodstarts.index(start)

        while self.periods[periodstarts[i]] <= end:
            period.append(i)
            i += 1
            if i == len(self.periods):
                break

        event = {
            "summary": name,
            "description": description,
            "day": day,
            "periods": period,
        }

        for ii in event['periods']:
            self.table[day-1][ii-1] = event

        self.events.append(event)
        return event

    def addSlot(self, tkn):
        name = tkn[0]

class TT_frame(tk.Frame):
    def __init__(self, periods, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=NSEW,padx=5,pady=(5,0))
        
        for i in range(1,6):
            self.rowconfigure(i,weight=1)
        for i in range(1,11):
            self.columnconfigure(i,weight=1)
        
        Days = ['Mon','Tue','Wed','Thu','Fri']
        i=1
        for day in Days:
            Label(self,text=day,bd=2,relief='groove',background="#333333",foreground="#FFFFFF").grid(row=i,sticky='nsew')
            i+=1
            
        i=1
        for period in periods.keys():
            text = period.strftime('%H:%M')+" - "+periods[period].strftime('%H:%M')
            Label(self,text=text,bd=2,relief='groove',background="#333333",foreground="#FFFFFF").grid(row=0,column=i+math.floor(i/6),sticky='nsew')
            i+=1 
         
        B = Button(self,command= lambda : self.print(),background='#333333',relief='groove',bd=2)
        B.grid(row=0,column=0,sticky='nsew') 
            
    def drawPeriod(
            self, title, description, xy, colsp=1, rowsp=1):

        F = tk.Frame(self, bd=3, relief='groove',background='white')

        F.grid(
            row=xy[0]+1,
            column=xy[1]+1+math.floor(xy[1]/5),
            rowspan=rowsp,
            columnspan=colsp,
            sticky=NSEW,
        )

        T1 = Label(
            F,
            text=title,
            font=tk.font.Font(weight="bold", size=12),
            background='white'
        ).pack(fill='both', pady=(10, 0))

        T2 = Label(
            F,
            text=description,
            font = tk.font.Font(size=10),
            background='white'
        ).pack(fill='both', pady=(0, 8))
        
    def print(self):
        cap = tkcap.CAP(self.master)
        cap.capture("tt.png")
