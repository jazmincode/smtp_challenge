from datetime import datetime, timedelta



class Utils:
    def __init__(self):
         pass
    
    def is_dictionary_full(self,dictionary):
        
        if isinstance(dictionary, dict) and len(dictionary) > 0:
            return True
        else:
            return False
        

    def add_to_timestamp(self,timestamp, rate, unit):
        if isinstance(timestamp, int):
            timestamp = datetime.fromtimestamp(timestamp)

        delta = timedelta(**{unit: rate})
        new_timestamp = timestamp + delta
        new_timestamp = int(new_timestamp.timestamp())
        return new_timestamp



