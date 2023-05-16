from django.db import models

# Create your models here

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_negatives(value):
    if value <= 0:
        raise ValidationError(
            _('Score cannot be less than Zero'),
            params={'value': value},
        )

class Country(models.Model):
    country_name = models.CharField( max_length=100)
    class Meta:

        verbose_name_plural = "Countries"

    def __str__(self):
        return self.country_name

class course_levels(models.Model):

    levels = models.CharField(max_length=100)
    def __str__(self):
        return self.levels
        
    class Meta:
        verbose_name = 'Course Level'


class current_education(models.Model):

    current_education = models.CharField(max_length=100)
    def __str__(self):
        return self.current_education
    class Meta:
        verbose_name = "Current Education"
        verbose_name_plural = "Current Education"

class intake(models.Model):

    intake_month = models.CharField(max_length=10)
    intake_year = models.IntegerField()
    def __str__(self):
        return f"{self.intake_month}-{self.intake_year}"

class documents_required(models.Model):

    docu_name = models.CharField(max_length=100)
    def __str__(self):
        return self.docu_name

    class Meta:
        verbose_name = "Documents required"
        verbose_name_plural = "Documents required"
        
class course_requirements(models.Model):

    requirement = models.CharField(max_length=100)
    def __str__(self):
        return self.requirement
        
    class Meta:
        verbose_name = "Course Requirement"
        verbose_name_plural = "Course Requirements"

    # class Meta:
    #     verbose_name_plural = "Course requirements"

class enquiry_status(models.Model):
    status = models.CharField(max_length=100)
    desciption = models.CharField(blank=True, null=True, max_length=1000)

    def __str__(self):
        return self.status
        
    class Meta:
        verbose_name = "Enquiry Status"
        verbose_name_plural= "Enquiry Status"

class application_status(models.Model):
    App_status = models.CharField(max_length=100)
    desciption = models.CharField(blank=True, null=True, max_length=1000)

    def __str__(self):
        return self.App_status
        
    class Meta:
        verbose_name = "Application Status"
        verbose_name_plural = 'Application Status'


from django.utils.translation import gettext_lazy as _


class Location(models.Model):
    location_name = models.CharField(_("Location Name"), max_length=50)
    

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __str__(self):
        return self.location_name

class Campus(models.Model):
    campus_name = models.CharField(_("Campus Name"), max_length=50)
    
    def __str__(self):
        return self.campus_name
    
class Payment_Option(models.Model):
    payment_type = models.CharField(_("Payment type"), max_length=100)
    
    def __str__(self):
        return self.payment_type

class Agent_Appointment(models.Model):
    agent_appointment = models.CharField(max_length=50)
    
    
class EnglishTest(models.Model):
    english_test = models.CharField(max_length=50)
    

    class Meta:
        verbose_name = _("English Test")
        verbose_name_plural = _("English Tests")

    def __str__(self):
        return self.english_test

    # def get_absolsst_detail", kwargs={"pk": self.pk})

class english_requirments(models.Model):
    english_tests = models.CharField( max_length=50)

    def __str__(self):
        return self.english_tests
        
class boardNotEligible(models.Model):
    board_name = models.CharField(_("Boards"), max_length=50)

    def __str__(self):
        return self.board_name
    



