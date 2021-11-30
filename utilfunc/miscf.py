from datetime import datetime, timedelta
import re

def extracttime(text):
    xpm = re.findall(r"([0-2]?[0-9]):?([0-6]?[0-9]?)(am|pm|AM|PM)?",text)[0]
    hh = int(xpm[0])
    mm = xpm[1]
    if mm == '':
        mm = 0
    else:
        mm = int(mm)
    if (xpm[2] == 'pm' or xpm[2] == 'PM') and not hh == 12:
        hh += 12
    if hh > 23:
        return 
    
    dttime = datetime(2000,1,1,hh,mm)
    return dttime
    
def extractduration(text):
    xpm = re.findall(r"([0-9]*):?([0-6]?[0-9]?)(h|hour)?S?(m|min|minute)?s?",text.lower())[0]
    hour = int(xpm[0])
    if xpm[1] == '':
        minute = 0
    else:
        minute = int(xpm[1])
    if not xpm[3] == '':
        dur= timedelta(minutes=hour,seconds=minute)
    else:
        dur= timedelta(hours=hour,minutes=minute)
    
    return dur

def extractday(text):
    if text in ['mon', 'Mon', 'Monday', 'monday', '1']:
        return 1
    if text in ['tue', 'Tue', 'Tuesday', 'tuesday', '2']:
        return 2
    if text in ['wed', 'Wed', 'Wednesday', 'wednesday', '3']:
        return 3
    if text in ['thu', 'Thu', 'Thursday', 'thursday', '4']:
        return 4
    if text in ['fri', 'Fri', 'Friday', 'friday', '5']:
        return 5
    if text in ['sat', 'Sat', 'Saturday', 'saturday', '6']:
        return 6
    if text in ['sun', 'Sun', 'Sunday', 'sunday', '7']:
        return 7
    return 0
