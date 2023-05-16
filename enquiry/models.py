from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from notifications.signals import notify
from django.conf import settings
from crum import get_current_user
# from pytz import timezone
from django.utils import timezone
import datetime 
from django.urls import reverse
# Create your models here.
from django.utils.translation import gettext_lazy as _

from master.models import *

from django.contrib.auth import get_user_model

from django.contrib.contenttypes.fields import GenericRelation

from comment.models import Comment
# Create your models here.


class PhoneNumbers(models.Model):
    phone_number = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='phno')

    def __str__(self):
        return self.phone_number

class University(models.Model):

    univ_name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    univ_desc = models.CharField(max_length=1000)
    univ_logo = models.ImageField(upload_to="universitylogo",blank=True)
    univ_phone = models.CharField(max_length=50, blank=True)
    univ_email = models.EmailField(max_length=254, blank=True)
    univ_website = models.URLField(blank=True)
    assigned_users = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default="")
    active = models.BooleanField(_("Is Active"), default=True)

    def __str__(self):
        return self.univ_name

    class Meta:
        verbose_name_plural = "Universities"


class Course(models.Model):

    university = models.ForeignKey(University, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    course_levels = models.ForeignKey(course_levels, on_delete=models.CASCADE)
    # intake = models.ForeignKey(intake, on_delete=models.CASCADE)
    intake = models.ManyToManyField(intake)
    documents_required = models.ForeignKey(documents_required, on_delete=models.CASCADE)
    course_requirements = models.ForeignKey(course_requirements, on_delete=models.CASCADE)
    Active = models.BooleanField()

    def __str__(self):
        return self.course_name
        
    def get_absolute_url(self):
        return reverse("enquiry-detail", kwargs={"pk": self.pk})
        
Course.objects.select_related().all()


class enquiry(models.Model):

    student_name = models.CharField(max_length=100)
    student_phone = models.CharField(max_length=20)
    student_email = models.EmailField()
    student_address = models.TextField()
    current_education = models.ForeignKey(current_education, on_delete=models.CASCADE ,null=True, blank=True)
    country_interested = models.ForeignKey(Country, on_delete=models.CASCADE,null=True, blank=True)
    university_interested = models.ForeignKey(University, on_delete=models.CASCADE,null=True, blank=True,limit_choices_to={'active':True,})
    level_applying_for = models.ForeignKey(course_levels, on_delete=models.CASCADE,null=True, blank=True)
    course_interested = models.ForeignKey(Course, on_delete=models.CASCADE, limit_choices_to={'Active':True,'university__active':True}, related_name= 'courses',null=True, blank=True)
    intake_interested = models.ForeignKey(intake, on_delete=models.CASCADE,null=True, blank=True)
    
    assigned_users = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True, limit_choices_to={"is_active": True})
    
    enquiry_status = models.ForeignKey(enquiry_status, on_delete=models.CASCADE,null=True, blank=True)
    added_by = models.ForeignKey(User,  null=True ,on_delete=models.SET_NULL, related_name="added_by")
    notes = models.TextField(null=True, blank=True)
    date_created = models.DateField(auto_now_add=True, null=True, blank=True)

    comments = GenericRelation(Comment)

    class MarriedChoices(models.TextChoices):
        YES = True, _('Yes')
        NO = False, _("No")
        
        
    passport_number = models.CharField(_("Passport Number"), max_length=50, default='0000',null=True, blank=True)
    dob = models.DateField(_("Date of Birth"), auto_now=False, auto_now_add=False,null=True, blank=True)
    married = models.CharField(_("Married"), choices= MarriedChoices.choices,default=MarriedChoices.NO, max_length=50)
    nationality = models.CharField(_("Nationality"), max_length=50, default='Indian',null=True, blank=True)


    def __str__(self):
        return self.student_name

    class Meta:
        verbose_name_plural = "Enquiries"

    def get_absolute_url(self):
        return reverse("enquiry-detail", kwargs={"pk": self.pk})
        
    def LastComment(self):
        qs = Comment.objects.filter(content_type=17, object_id = self.id)
        if qs.exists():
            
            return qs[0]
        else:
            return "-"


# @receiver(post_save, sender=enquiry)
# def send_appointment_confirmation_email(sender, instance, created, **kwargs):
#     if created:
#         # change fail_silently = True if want to see errors while sending email.

#         send_mail(
#             'Confirmation Email',
#             "Here is the message",
#             settings.EMAIL_HOST_USER,
#             [instance.student_email, instance.assigned_users.email],
#             fail_silently= False,
#         )
#         print('email sent successfully')
#     else:
#         return



# @receiver(post_save, sender=enquiry)
# def send_notification(sender, instance, created, **kwargs):
#     notify.send(sender,
#     recipient= instance.assigned_users,
#     verb= instance.student_name,
#     description = f"A new enquiry with name {instance.student_name} has been assigned to you.",
#     # timestamp = timezone.now()
#     )
#     # notify.send(sender,recipient=instance, verb='was saved')

# post_save.connect(send_notification, sender=enquiry)



