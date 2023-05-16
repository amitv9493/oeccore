from django.contrib import admin
from .models import enquiry, University, Course
from import_export.admin import ImportExportMixin
from .forms import enquiryForm
from django.db.models import Q
from django.utils.html import format_html

# FOR CHART.JS

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.functions import TruncDay
from django.db.models import Count
from django.utils.translation import gettext_lazy as _


# Register your models here.

# enquiryform = select2_modelform(enquiry, attrs={'width':'250px'})


class EnquiryList(admin.ModelAdmin):
    ordering = ("-date_created",)
    radio_fields = {'married':admin.HORIZONTAL}

    date_hierarchy = "date_created"
    form = enquiryForm

    list_display = (
        'student_name', 'student_phone', 'student_email', 'current_education', 'country_interested', 'university_interested',
        'course_interested', 'level_applying_for', 'intake_interested', 'assigned_users', 'added_by', 'notes','LastComment','date_created')

    list_filter = ['university_interested','level_applying_for','intake_interested',]


    exclude = ['added_by']
    list_display_links = ['student_name']
    list_per_page = 10
    search_fields = ['university_interested__univ_name', ]


    autocomplete_fields = [

        # 'course_interested',
        'university_interested',
        'level_applying_for',
        'current_education',
        'level_applying_for',
        'intake_interested',
        'assigned_users',
        'enquiry_status',
        'country_interested'

    ]
    
    fieldsets = (
        ('Student Info', {
            "fields": (
                'student_name',
                'student_phone',
                'student_email',
                'student_address',
                'current_education',
                'country_interested',
                
                'passport_number',
                'dob',
                'married',
                'nationality',
            ),
        }),

        ("Course Info", {
            "fields": (
                'university_interested',
                'level_applying_for',
                'course_interested',
                'intake_interested',
                'notes',

            )
        }),

                ("Assigned Enquiry", {
            "fields": (
                'assigned_users',
                'enquiry_status',
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(Q(added_by=request.user) | Q(assigned_users=request.user)
                         )
        
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        queryset = response.context_data["cl"].queryset
        chart_data = self.chart_data(queryset)
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        response.context_data.update({"chart_data": as_json})
        return response


    def chart_data(self, queryset):
        return (
            queryset.annotate(date=TruncDay("date_created"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )




admin.site.register(enquiry, EnquiryList)


class UniversityListAdmin(ImportExportMixin, admin.ModelAdmin):

    def university_logo(self, obj):
        try:
            return format_html('<img src="{}" style="max-width:80px; max-height:80px"/>'.format(obj.univ_logo.url))
        except ValueError:
            return
    list_display = (
        'univ_name', 'country', 'univ_desc', 'university_logo', 'univ_phone', 'univ_email','active',
        'univ_website', 'assigned_users')

    list_filter = ('univ_name','active', 'country', 'univ_desc', 'univ_logo',
                   'univ_phone', 'univ_email', 'assigned_users')

    search_fields = ['univ_name']
    autocomplete_fields = [
        'assigned_users',
        'country',
    ]
    list_display_links = ['univ_name']
    list_per_page = 10


admin.site.register(University, UniversityListAdmin)


class CourseListAdmin(ImportExportMixin, admin.ModelAdmin):
    
    def Intake(self,obj):
        return ",".join([f'{i.intake_month}-{i.intake_year}' for i in obj.intake.all()])
        
    list_display = ('course_name','university', 'course_levels',
                    'Intake', 'documents_required', 'course_requirements', 'Active')

    list_filter = ('university', 'course_levels',
                   'intake', 'documents_required',
                   'course_requirements', 'Active',
                   'university__active')

    # list_display_links = None
    list_per_page = 20

    search_fields = ['course_name']

    autocomplete_fields = [
        'university',
        'course_levels',
        'intake',
        'documents_required',
        'course_requirements',


    ]

admin.site.register(Course, CourseListAdmin)

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import PhoneNumbers

class PhoneNumbersInline(admin.StackedInline):
    model = PhoneNumbers
    can_delete = False
    verbose_name_plural = 'Phone Numbers'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (PhoneNumbersInline,)
    agent_fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        # No permissions
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (_("Groups"), {"fields": ("groups",)}),
    )

    agent_fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                )
            },
        ),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        # Removing the permission part
        (
            _("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "is_active",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        # Keeping the group parts? Ok, but they shouldn't be able to define
        # their own groups, up to you...
        (_("Groups"), {"fields": ("groups",)}),
    )
    # user_group = (Group.objects.get(user=request.user.id)).name
    # if user_group == 'Agent':

    def change_view(self, request, *args, **kwargs):
        # for non-superuser
        if not request.user.is_superuser:
            try:
                self.fieldsets = self.agent_fieldsets
                response = super(UserAdmin, self).change_view(request, *args, **kwargs)
            finally:
                # Reset fieldsets to its original value
                self.fieldsets = UserAdmin.fieldsets
            return response
        else:
            return super(UserAdmin, self).change_view(request, *args, **kwargs)
        


    # def get_fieldsets(self, request, obj=None):
    #     if not request.user.is_superuser:
    #         return self.agent_fieldsets
    #     else:
    #         return super(UserAdmin, self).get_fieldsets(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(is_superuser=False).exclude(groups__name="Branch")
            return qs

        else:
            return qs

    # def formfield_for_foreignkey(self, db_field, request, **kwargs): #type:ignore
    #     qs =  super().formfield_for_foreignkey(db_field, request, **kwargs)
    #     print(db_field.name)
    #     if db_field.name == 'groups':
    #         if Group.objects.get(user = request.user.id).name == "Admins":

    #             kwargs['queryset'] = Group.objects.filter(name= "Agent")

    #         elif Group.objects.get(user = request.user.id).name == "Agent":
    #             kwargs['queryset'] = Group.objects.exclude(name= "Admins")

    #         else:
    #             return qs

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        try:
            if db_field.name == "groups":
                user = request.user
                print(user.id)

                try:
                    user_group = (Group.objects.get(user=user.id)).name
                except Group.DoesNotExist:
                    user_group = None

                print(user_group)

                if user_group == "Branch":
                    kwargs["queryset"] = Group.objects.filter(name="Agent")
                
                if user_group == "Agent":
                    print("agent ran")
                    kwargs["queryset"] = Group.objects.exclude(name="Branch").exclude(name="superuser")

                if user_group == "superuser":
                    print("supersuer ran")
                    kwargs["queryset"] = Group.objects.all()

                if user_group == None:
                    kwargs["queryset"] = Group.objects.none()

            return super().formfield_for_manytomany(db_field, request, **kwargs)
        
        except KeyError:
            # kwargs["queryset"] = Group.objects.all()
            
            return super().formfield_for_manytomany(db_field, request, **kwargs)
            


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)






