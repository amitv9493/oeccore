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
    
class UniversityRequirements(models.Model):
    
    class appointmemt_choices(models.TextChoices):
        YES = 'YES'
        NO = 'NO'
        UNIVERSITY_DISCREATION = 'University Discretion'

    class yes_no_only(models.TextChoices):
        YES = 'YES'
        NO = 'NO'
    '''GENERAL INFORMATION'''

    university_name = models.ForeignKey("enquiry.University", verbose_name=_("University Name"), on_delete=models.CASCADE)
    course_level = models.ForeignKey(course_levels, on_delete=models.SET_NULL, null=True)

    location = models.ManyToManyField(Location, verbose_name=_("Locations"))
    campus = models.ManyToManyField(Campus)
    intake = models.ManyToManyField(intake)
    general_documents = models.ManyToManyField(documents_required, related_name="university_requirements")
    mandatory_docs = models.ManyToManyField(documents_required, verbose_name=_("Mandatory Document"), related_name="university_requirement")

    finance_for_CAS = models.CharField(_("Finance for CAS"), default=True, blank=True, choices=yes_no_only.choices, max_length=10)
    credibility_interview = models.CharField(_("Credibility Interview"), default=True, blank=True, choices=yes_no_only.choices, max_length=10)
    
    offer_timeline = models.CharField(_("Offer time line"), max_length=100)
    payment_option = models.ManyToManyField(Payment_Option, verbose_name=_("Payment Option"))
    deposit_for_CAS = models.CharField(_("Deposit for CAS"), max_length=50)
    scholarship = models.CharField(_("Scholarship"), max_length=100)
    appointment_of_agent = models.CharField(_("Appointment of agent"), max_length=50, choices= appointmemt_choices.choices)
    change_of_agent = models.CharField(_("Change of agent"), max_length=50, choices= appointmemt_choices.choices)
    amount = models.CharField(max_length=50, blank=True)
    app_fees = models.CharField(_("Application Fees"), max_length=50, null=True, blank=True)

    dependent_acceptance = models.CharField(_("Dependent Acceptance"), max_length=100)

    accept_case_from_high_risk = models.CharField(_("Accept Case from High Risk"), max_length=50)
    general_visa_refusal = models.CharField(_("General Visa Refusal type"), max_length=100)
    student_visa_refusal = models.CharField(_("Student Visa Refusal type"), max_length=100)
    english_test = models.ManyToManyField( EnglishTest,verbose_name=_("English Test Accepted"))
    web_link = models.URLField(default=None, null=True)

    '''ACADEMIC REQURIEMENTS'''
    
    english_waiver =  models.PositiveIntegerField(_("English Waiver-(Percent)"))
    english_requirement = models.ManyToManyField(english_requirments,)
    academic_requirement = models.PositiveIntegerField(_(" Academic Requirement General(Percent)")) 
    
    ielts_score = models.DecimalField(_("IELTS"), validators= [validate_negatives],decimal_places=1,max_digits=3 )
    tofel = models.DecimalField(_("TOFEL"), validators= [validate_negatives],decimal_places=1,max_digits=3)
    pte = models.DecimalField(_("PTE"), validators= [validate_negatives],decimal_places=1,max_digits=3)
    
    others = models.CharField(_("Others"), max_length=50)
    board_not_eligible = models.ManyToManyField(boardNotEligible, verbose_name=_("Region or Boards not Eligible for English Waiver"),)
    gap = models.PositiveIntegerField(_("Education GAP (In years)"), )

    placement_option = models.CharField(_("Placement Option "), max_length=50, choices=yes_no_only.choices, default=yes_no_only.NO)
    dependency_acceptance = models.CharField(_("Dependent Acceptance"), max_length=50, choices=yes_no_only.choices, default=yes_no_only.NO)



