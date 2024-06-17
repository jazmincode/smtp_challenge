from app.data_manager import DataManager
from app.utils import Utils
from typing import List
from datetime import datetime
from config import SendMail,Type,Sended,User
from pydantic import ValidationError




class Validator(DataManager,Utils):

    def __init__(self):
        pass


    def rate_delimitated(self, 
                         data:SendMail # this param bring the data (type, email) to evaluate before send notification
                         ):  

        try:

            data = SendMail(**data) # evaluate if data have the right structure
        except ValidationError as e:
            return False,{"error":str(e).encode("utf-8")}	
        
        
        data_validated=self.data_validate(data) 
        
        if data_validated and isinstance(data_validated, dict): # Found the same type of email sent in the past to the same user

            return  self.timing_is_ok(data_validated),data_validated #evaluate if the rate of time is done
        
        elif data_validated: # Not Found so this is the first time to send this email to this user
            return True, None

        
        return False,data_validated
                
    
    def data_validate(self, 
                      data:SendMail # data request to send notification
                      ):
        
        data_evaluated=None

        real_user=self.exist("users",data.email,"email") # is this user in our data?

        
        real_type=self.exist("type_message_rate",data.type,"type_id") ## is this type in our data?
        
       
        if self.is_dictionary_full(real_user) and self.is_dictionary_full(real_type): 

            data_evaluated=self.emails_were_sended(real_user,real_type) 
            
            if self.is_dictionary_full(data_evaluated): 
                return data_evaluated
            
            else: 

                new ={
                    "user_id": real_user['user_id'],
                    "type_id": real_type['type_id'],
                    "sended_at": int(datetime.now().timestamp())
                }

                self.add_sended("sended_time",new)

                return True

        return data_evaluated
    

      

    def exist(self,
              element:str, # key to find the List and evaluate
              value:str, # value to find
              key:str): # key to search in the dict
        try:
            
            result=self.filter_regular(element,key,value)[0]
        except:
            return None
        return result
    
    def emails_were_sended(self,
                           user:User, # user email
                           type:Type,): # type of message
        
       
        try:

            user = User(**user) 
            type = Type(**type)

        except ValidationError as e:
            return str(e)
        
       
        
        try:

            sended=self.get_sended("sended_time",user.user_id,type.type_id)[0]
            
        except:
            return None
        
        return sended

    
    def timing_is_ok(self,
                     sended:Sended # dict with info about the last email of this type sent to the same user
                     ):

        types_list=self.read_key("type_message_rate")
        item=self.filter_name(types_list,"type_id",sended["type_id"])

        rate= item["rate"] 
        unit=item["unit"]

        time_must_pass = self.add_to_timestamp(sended["sended_at"],rate, unit)
        now_timestamp = int(datetime.now().timestamp())
    
        if time_must_pass < now_timestamp: 
            return True
        else:
            return False
        

    
        

        
       

            

    
            

            




    


        
        