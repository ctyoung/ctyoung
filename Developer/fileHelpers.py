# File helpers

import datetime
import json

def fileRead(file):
    with open(file, 'r') as f:
        allData = json.load(f)
    return allData

def fileWrite(file, dataToWrite):
    formatDates = lambda obj: (obj.isoformat() 
            if isinstance(obj, datetime.datetime) 
            or isinstance(obj, datetime.date) 
            else None)
    with open(file, 'w') as f:
        json.dump(dataToWrite, f, default=formatDates)
        
