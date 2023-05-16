from django.urls import reverse
from oeccore import settings
from django.contrib import admin
from .models import Application
from import_export.admin import ImportExportMixin
from django.utils.html import mark_safe
from django.utils.html import format_html
from io import BytesIO
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import get_template
# from xhtml2pdf import pisa
import os 
from django.shortcuts import render
from django.http import HttpResponseRedirect

import json

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay

# Create your views here.


class Application_list(ImportExportMixin, admin.ModelAdmin):
    date_hierarchy = "created_at"
    import_export_change_list_template = 'admin/application/application/change_list.html'

    ordering = ("-created_at",)  
    def tenth_marksheet(self, obj):
        try:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.Tenth_Marksheet.url))
        except ValueError:
            return

    def twelveth_marksheet(self, obj):
        try:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.Twelveth_Marksheet.url))
        except ValueError:
            return

    def diploma_marksheet(self, obj):
        try:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.Diploma_Marksheet.url))
        except ValueError:
            return

    def bachelor_marksheet(self, obj):
        try:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.Bachelor_Marksheet.url))
        except ValueError:
            return

    # def masters_marksheet(self, obj):
    #     try:
    #          x= format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.Master_Marksheet.url))
             
    #     except ValueError:
    #         return
        
    def MasterMarksheet(self, obj):
        try:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.Master_Marksheet.url))
        except ValueError:
            return

    def lor(self, obj):
        try:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.Lor.url))
        except ValueError:
            return

    def sop(self, obj):
        try:
            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.Sop.url))
        except ValueError:
            return

    def resume(self, obj):
        try:

            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.Resume.url))

        except ValueError:
            return

    def language_exam(self, obj):
        try:

            return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.Language_Exam.url))
        except ValueError:
            return

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        queryset = response.context_data["cl"].queryset
        chart_data = self.chart_data(queryset)
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        response.context_data.update({"chart_data": as_json})
        return response
    
    def chart_data(self, queryset):
        return (
            queryset.annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        
    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            Application.objects.annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)
        
    tenth_marksheet.allow_tags = True

    list_display = ['name', 'tenth_marksheet', 'twelveth_marksheet', 'diploma_marksheet', 'bachelor_marksheet',
                    'MasterMarksheet', 'lor', 'resume', 'language_exam', 'assigned_users', 'status','LastComment']


    # fields = ('name', 'tenth_marksheet', 'Twelveth_Marksheet', 'Diploma_Marksheet', 'Bachelor_Marksheet',
    #           'Master_Marksheet', 'Lor', 'Resume', 'Language_Exam', 'assigned_users', 'status',)

    list_filter = ('name', 'assigned_users', 'status',)
    # readonly_fields = ['tenth_marksheet'] # to show the image preview field in edit page.
    list_display_links = ('name',)
    list_per_page = 20
    autocomplete_fields = ['name']

    actions = ['export_as_pdf']


    '''export as pdf view'''

    def export_as_pdf(self, request,queryset, *args, **kwargs):
        q= queryset.all()
        global qid
        try:

            q= q[0].id

        except:
            raise ValueError("please select only one Application")
        

        # pdf = render_to_pdf('pdf/pdf.html', context_dict=context)
        # return HttpResponse(pdf, content_type='application/pdf')
        # return redirect('pdf')
        # return render(request, 'pdf/pdf.html', context=context)
        return HttpResponseRedirect(reverse('pdf', kwargs={'pk':q,}))


    # export_as_pdf.action_type =1
    # # export_as_pdf.action_url = q
    
    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)


    export_as_pdf.confirm = None
    export_as_pdf.icon = 'fas fa-download'
admin.site.register(Application, Application_list)

