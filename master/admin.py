from django.contrib import admin

# Register your models here.
from .models import *
from import_export.admin import ImportExportMixin

# from notifications.models import notifications

# admin.site.unregister(notifications)
# Register your models here.


# class CourseListAdmin(ImportExportMixin, admin.ModelAdmin):
#     list_display = ('university', 'course_name', 'course_levels', 'intake', 'documents_required', 'course_requirements', 'Active')

#     list_filter = ('university', 'course_name', 'course_levels', 'intake', 'documents_required', 'course_requirements', 'Active')

#     list_display_links = None
#     list_per_page = 20



# class UniversityListAdmin(ImportExportMixin, admin.ModelAdmin):
#     list_display = (
#         'univ_name', 'country', 'univ_desc', 'univ_logo', 'univ_phone', 'univ_email',
#         'univ_website', 'assigned_users')

#     list_filter = ('univ_name', 'country', 'univ_desc', 'univ_logo', 'univ_phone', 'univ_email', 'assigned_users')

#     list_display_links = None
#     list_per_page = 10
# admin.site.register(university, UniversityListAdmin)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ['country_name']


@admin.register(course_levels)
class course_levelsAdmin(admin.ModelAdmin):
    search_fields = ['levels']


@admin.register(intake)
class intakeAdmin(ImportExportMixin, admin.ModelAdmin):
    search_fields = ['intake_month']

@admin.register(current_education)
class current_educationAdmin(admin.ModelAdmin):
    search_fields = ['current_education',]


@admin.register(documents_required)
class documents_requiredAdmin(admin.ModelAdmin):
    search_fields = ['docu_name',]

@admin.register(course_requirements)
class course_requirementsAdmin(admin.ModelAdmin):
    search_fields = ['requirement',]

@admin.register(enquiry_status)
class enquiry_statusAdmin(admin.ModelAdmin):
    list_display = ['status','desciption']
    search_fields = ['status',]

@admin.register(application_status)
class application_statusAdmin(admin.ModelAdmin):
    list_display = ['App_status','desciption']
    search_fields = ['App_status',]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "location_name")


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ("id", "campus_name")


@admin.register(Payment_Option)
class Payment_OptionAdmin(admin.ModelAdmin):
    list_display = ("id", "payment_type")


@admin.register(Agent_Appointment)
class Agent_AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "agent_appointment")


@admin.register(EnglishTest)
class EnglishTestAdmin(admin.ModelAdmin):
    list_display = ("id", "english_test")


@admin.register(english_requirments)
class english_requirmentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'english_tests')


@admin.register(boardNotEligible)
class boardNotEligibleAdmin(admin.ModelAdmin):
    list_display = ('id', 'board_name')


# class UniversityRequirementsAdmin(ImportExportMixin, admin.ModelAdmin):
#     radio_fields = {"finance_for_CAS": admin.HORIZONTAL}
#     lsit_display_links = ['university_name']
#     list_display = (
#     'university_name',
#     'course_level',
#     'finance_for_CAS',
#     'credibility_interview',
#     'offer_timeline',
#     'deposit_for_CAS',
#     'scholarship',
#     'appointment_of_agent',
#     'change_of_agent',
#     'amount',
#     'app_fees',
#     'dependent_acceptance',
#     'accept_case_from_high_risk',
#     'general_visa_refusal',
#     'student_visa_refusal',
#     'web_link',
#     'english_waiver',
#     'academic_requirement',
#     'ielts_score',
#     'tofel',
#     'pte',
#     'others',
#     'gap',
#     'placement_option',
#     'dependency_acceptance',
# )
 
#     list_filter = (
#         "university_name",
#         "finance_for_CAS",
#         "credibility_interview",
#     )


#     fieldsets = (
#         (
#             "General Information",
#             {
#                 "fields": (
#                     "university_name",
#                     'course_level',
#                     'location',
#                     'campus',
#                     'intake',
#                     'general_documents',
#                     'mandatory_docs',
                    
#                     "finance_for_CAS",
#                     "credibility_interview",
                    
#                     "offer_timeline",
#                     'payment_option',
#                     "deposit_for_CAS",
#                     "scholarship",
#                     "appointment_of_agent",
#                     "change_of_agent",
#                     "amount",
#                     "app_fees",
                    
#                     "dependent_acceptance",
                    
#                     "accept_case_from_high_risk",
#                     "general_visa_refusal",
#                     "student_visa_refusal",
#                     'english_test',
#                     "web_link",
#                 ),
#             },
#         ),
#         (
#             "Academic Requirement",
#             {
#                 "fields": (
#                     "english_waiver",
#                     "english_requirement",
#                     "academic_requirement",
                    
#                     "ielts_score",
#                     "tofel",
#                     "pte",
                    
#                     "others",
#                     "board_not_eligible",
#                     "gap",
                    
#                     "placement_option",
#                     "dependency_acceptance",
#                 ),
#             },
#         ),
#     )

