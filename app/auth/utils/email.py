from app import mail
from flask_mail import Message
from flask import current_app, render_template
from threading import Thread

#allow messages to be sent asynchronously using thread
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

#Create a function to send email messages
def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    #Create Email message
    msg = Message(app.config['SMS_MAIL_SUBJECT_PREFIX'] + '' + subject, 
                    sender=app.config['SMS_MAIL_SENDER'], recipients=[to])
    
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    #Asynchronous mail support
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
