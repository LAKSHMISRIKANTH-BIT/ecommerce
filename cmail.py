import smtplib
from email.message import EmailMessage
def send_mail(to, subject, body):
    server=smtplib.SMTP_SSL('smtp.gmail.com',465) #object creation for gmail server
    server.login('lakshmisrikanth2004@gmail.com','jrrr rodz zdhs vzxo') #login to email
    msg=EmailMessage()#email format object creation
    msg['FROM']='lakshmisrikanth2004@gmail.com'
    msg['TO']=to
    msg['SUBJECT']=subject
    msg.set_content(body)
    server.send_message(msg)#mail sending
    server.close()#closing the server object