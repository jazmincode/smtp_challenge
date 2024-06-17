import json
from typing import List
from datetime import datetime
from config import Sended                                                                       

class DataManager:

    def __init__(self):
        self.data = None

    def _read(self):
        with open('data/data.json', 'r') as f:
            self.data = json.load(f)
        return self.data

    def _write(self):
        with open('data/data.json', 'w') as f:
            state = json.dump(self.data, f, indent=4)
            return state
        
    def read_key(self, key:str):
        return self.data[key]

    
    def filter_regular(self,list_from:str,key:str, value:str):
        self._read()
        result = [element for element in self.data[list_from] if element.get(key) ==  value]
        return result
    
    def get_sended(self,key:str, user_id:int,type_id:int):
        sended_list= self.read_key(key)
        sended = [element for element in sended_list if element['user_id'] == user_id and element['type_id']== type_id]
        return sended
    
    def modify_sended(self,sended:Sended):
        for element in self.data['sended_time']:
            if element['user_id'] == sended['user_id'] and element['type_id']== sended['type_id']:
                element['sended_at'] = int(datetime.now().timestamp())
        state= self._write()
        return state
    
    def add_sended(self,key:str,data:Sended):
        self.data[key].append(data) 
        state= self._write()
        return state
        

    def filter_name(self, list:list, key:str, value:int):
        found = None
        for item in list:
            if item.get(key) == value:
                found = item
                break
        
        return found
    
    
    

    
        





  