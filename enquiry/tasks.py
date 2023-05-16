from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
import os

logger = get_task_logger(__name__)




@shared_task
def send_appointment_confirmation_email(context,*args, **kwargs):
    email_subject = "Confirmation Email"
    email_body = get_template("emails/html/index.html").render(context=context)

    email = EmailMultiAlternatives(
        email_subject,
        email_body,
        context['sender'],
        context['recicpent_list'],
    )
    
    email.mixed_subtype = 'related'
    email.attach_alternative(email_body, "text/html")
    img_dir = 'static/emails/images/'
    image = 'logo.png'
    file_path = os.path.join(img_dir,image)
    
    with open (file_path, 'rb') as f:
        img  = MIMEImage(f.read())
        img.add_header('Content-ID', '<{name}>'.format(name=image))
        img.add_header('Content-Disposition', 'inline', filename=image)
    
    email.attach(img)
        
    email.send(fail_silently=False)
    
    print("Email sent successfully")

    logger.info("sent email ")

    
        