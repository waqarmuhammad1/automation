import threading
import smtpd
import asyncore
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def SendResultEmail():
    sender_email = 'results.testcase@gmail.com'
    sender_password = '$admin1234$'
    recipient_email = 'maria.mushtaq581@gmail.com'
    subject = 'Test Case Result'
    body = 'Status : ''Passed'''

    obj_EmailSender = EmailSender(sender_email, sender_password, recipient_email,subject,body)
    obj_EmailSender.send_email()

class EmailSender():

    def __init__(self, sender_email, sender_password, recipient_email,subject,body):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email
        self.subject = subject
        self.body = body

    def get_plaintext_message(self,FROM,TO,SUBJECT,TEXT):
        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        return message

    def get_html_message(self,FROM,TO,SUBJECT,TEXT):

        msg = MIMEMultipart('alternative')

        msg['Subject'] = SUBJECT
        msg['From'] = FROM
        msg['To'] = TO

        # Create the body of the message (a plain-text and an HTML version).

        html = '''\
                <html>
                  <head></head>
                  <body>
                    <p>This is a test message.</p>
                    <p>Text and HTML</p>
                  </body>
                </html>
                '''

        html_message = MIMEText(html, 'html')
        msg.attach(html_message)

        return msg

    def send_email(self):
        gmail_user = self.sender_email
        gmail_pwd = self.sender_password
        FROM = self.sender_email
        TO = self.recipient_email if type(self.recipient_email ) is list else [self.recipient_email ]
        SUBJECT = self.subject
        TEXT = self.body

        msg = self.get_plaintext_message(FROM,TO,SUBJECT,TEXT)

        #html_message = self.get_html_message(FROM,TO,SUBJECT,TEXT)

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, msg)
            server.close()
            print('successfully sent the mail')
        except:
            print('failed to send mail')



#if __name__ == '__main__':

#    sender_email = 'results.testcase@gmail.com'
#    sender_password = '$admin1234$'
#    recipient_email = 'maria.mushtaq581@gmail.com'
#    subject = 'Test Case Result'
#    body = 'Status : ''Passed'''

#    obj_EmailSender = EmailSender(sender_email, sender_password, recipient_email,subject,body)
#    obj_EmailSender.send_email()
