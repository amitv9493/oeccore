from django.db import models
from notifications.base.models import AbstractNotification
from enquiry.models import enquiry
from master.models import application_status
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from django.urls import reverse
from comment.models import Comment
# Create your models here.
from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template

class Application(models.Model):

    name = models.ForeignKey(enquiry, on_delete=models.CASCADE, related_name='application')

    Tenth_Marksheet = models.ImageField(upload_to="images", null=True, blank=True)
    Twelveth_Marksheet = models.ImageField(upload_to="images", null=True, blank=True)
    Diploma_Marksheet = models.ImageField(upload_to="images", null=True, blank=True)
    Bachelor_Marksheet = models.ImageField(upload_to="images", null=True, blank=True)
    Master_Marksheet = models.ImageField(upload_to="images", null=True, blank=True)
    Lor = models.ImageField(upload_to="images", null=True, blank=True)
    Sop = models.ImageField(upload_to="images", null=True, blank=True)
    Resume = models.ImageField(upload_to="images", null=True, blank=True)
    Language_Exam = models.ImageField(upload_to="images",null=True, blank=True)
    assigned_users = models.ForeignKey(User, on_delete=models.CASCADE, default="", limit_choices_to={"is_active": True})
    status = models.ForeignKey(application_status, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,related_name="added_byForApplication", default=1)
    
    comments = GenericRelation(Comment)



    def __str__(self):
        return self.name.student_name

    def get_absolute_url(self):
        return reverse("application-detail", kwargs={"pk": self.pk})

    def LastComment(self):
        qs = Comment.objects.filter(content_type=18, object_id = self.id)
        if qs.exists():
            
            return qs[0]
        else:
            return "-"



@receiver(post_save, sender=Application)
def send_appointment_confirmation_email(sender, instance, created, **kwargs):
    if created:
        try:
            obj = enquiry.objects.get(student_name__icontains = instance.name.student_name)
            student_email = obj.student_email
        except:
            raise ValueError("More then 1 Student with the same name exits") 
        # change fail_silently = True if want to see errors while sending email.

        send_mail(
            'Confirmation Email',
            "Here is the message",
            settings.EMAIL_HOST_USER,
            [student_email, instance.assigned_users.email],
            fail_silently= True,
        )
        print('email sent successfully')
    else:
        print("email was not sent")




