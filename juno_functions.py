import json
from datetime import datetime
import pytz

class Juno_functions:
    available_functions = {}
    def __init__(self): 
        #append functions to available_functions
        self.available_functions = {
            "get_time": self.get_time,
        }
    
    def get_time(timezone):
        #get current time in said timezone
        time = {
            "timezone": timezone,
            "time": datetime.now(pytz.timezone(timezone)).strftime("%m/%d/%Y %H:%M:%S")
        }
        #return in json format
        return json.dumps(time)