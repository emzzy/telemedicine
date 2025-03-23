from django.core.mail import EmailMessage
import threading

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        try:            
            self.email.send()
        except Exception as e:
            print(f'email sending failed: {str(e)}')


class Util:
    @staticmethod
    def send_email(data):
        
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']],
            from_email="noreply@gmail.com"
        )
        try:
            EmailThread(email).start()
        except Exception as e:
            print(f'Email failed to send: {str(e)}')
