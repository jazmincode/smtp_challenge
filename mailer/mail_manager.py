from config import HOST, USERNAME, PASSWORD, PORT, SendMail,MailBody
from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP
from app.validator import Validator



class Mailer(Validator):
    def __init__(self):
        pass
    
    def build_email(self,data: SendMail):
        email = self.exist("type_message_rate",data.type,"type_id")
        
        return {"to": data.email, "subject": email["subject"], "body": email["message"]}

    def send_mail(self,data: SendMail | None = None):

        data = SendMail(**data)
        email = self.build_email(data)
        msg = MailBody(**email)

        message = MIMEText(msg.body, "html")
        message["From"] = USERNAME
        message["To"] = msg.to
        message["Subject"] = msg.subject
        
        ctx = create_default_context()

        try:
            with SMTP(HOST, PORT) as server:
                server.ehlo()
                server.starttls(context=ctx)
                server.ehlo()
                server.login(USERNAME, PASSWORD)
                server.send_message(message)
                server.quit()
            return {"status": 200, "errors": None}
        except Exception as e:
            return {"status": 500, "errors": e}