from fastapi import FastAPI, BackgroundTasks
from mailer.mail_manager import Mailer
from config import SendMail
from app.validator import Validator

val = Validator()

mailer = Mailer()

app = FastAPI(title="Envio de Notificaciones", description="Envia email por categoria y rate", version="1")


@app.get("/")
def index():
    return {"status": "mailserver is running."}


@app.post("/send-email")
def schedule_mail(request: SendMail, tasks: BackgroundTasks):

    data = request.dict()
    allowed,new_data = val.rate_delimitated(data)

    if allowed:
        tasks.add_task(mailer.send_mail, data)
        val.modify_sended(new_data) if new_data  else None

        return {"status": 200, "message": "email has been scheduled"}
    
    elif isinstance(new_data, dict) and "error" in new_data:
        return {"status": 500, "message": new_data['error']}
    
    elif not new_data:
        return {"status": 500, "message":"Value email or type don't exist"}
        
    else:
        return {"status": 403, "message": "You must wait for the right moment"}
    





