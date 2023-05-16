from django.db.models.signals import post_save
from .models import enquiry
from celery import shared_task
from django.dispatch import receiver
import os

from .tasks import send_appointment_confirmation_email

# @receiver(post_save,sender=enquiry)

# def call_email(sender, instance, created, **kwargs):
#     if created:
#         # change fail_silently = True if want to see errors while sending email.
#         context = {
#             "student_name": str(instance.student_name),
#             "assigned_user": str(instance.assigned_users),
#             "added_by": str(instance.added_by),
#             "phone": int(instance.student_phone),
#             "email": str(instance.student_email),
#             "course": str(instance.course_interested),
#             "intake": str(instance.intake_interested),
#             "recicpent_list": [instance.student_email, instance.assigned_users.email],
#             "sender":'info@flyurdream.online',
#         }

        
#         send_appointment_confirmation_email.delay(context=context)
        


from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives

from django.conf import settings

from django.template.loader import get_template
from email.mime.image import MIMEImage
# Create your models here.
from master.models import *

'''for signals modules'''

from django.template.loader import get_template

from email.mime.image import MIMEImage


from django.dispatch import receiver

from twilio.rest import Client

from oeccore.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

import os
import threading

class EmailThread(threading.Thread):
    
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()
                
        


@receiver(post_save, sender=enquiry)
def send_appointment_confirmation_email(sender, instance, created, **kwargs):
    if created:
        # change fail_silently = True if want to see errors while sending email.
        context = {
            "student_name": instance.student_name,
            "assigned_user": instance.assigned_users,
            "added_by": instance.added_by,
            "phone": instance.student_phone,
            "email": instance.student_email,
            "course": instance.course_interested,
            "intake": instance.intake_interested,
        }
        email_subject = "Confirmation Email"
        email_body = get_template("emails/html/index.html").render(context=context)

        email = EmailMultiAlternatives(
            email_subject,
            email_body,
            settings.EMAIL_HOST_USER,
            ["admissions@flyurdream.com",],
        )
        
        emails = "admissions@flyurdream.com"
        
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
        
        email.send(fail_silently=True)
        # EmailThread(email).start()

        
        # print("Email sent successfully")

