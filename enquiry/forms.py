from django import forms 
from .models import University, Course, enquiry
from django_select2.forms import ModelSelect2Widget
from .models import Course

# class enquiryForm(forms.ModelForm):
    
#     course_interested = forms.ModelChoiceField(
#         queryset=Course.objects.all().exclude(Active = False),
#         label='course interested',
#         widget=ModelSelect2Widget(
#             model=Course,
#             queryset=Course.objects.all().exclude(Active = False),
#             search_fields=['course_name__icontains'],
#             dependent_fields = {'university_interested':'university'},
#             attrs={'data-placeholder': 'Search for Courses', 'data-width': '250px'},

            
#             ))


from dal import autocomplete

from django import forms


class enquiryForm(forms.ModelForm):
    class Meta:
        model = enquiry
        fields = ('__all__')
        widgets = {
            'course_interested': autocomplete.ModelSelect2(url='course-autocomplete',forward=['university_interested','level_applying_for'],attrs={'data-placeholder': 'Select Course'})
        }