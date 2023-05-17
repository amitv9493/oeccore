
from django.contrib import admin
from django.urls import path, include
# import notifications.urls
from django.views.generic import TemplateView

from enquiry.views import *
# notification,
# markRead,
# seeAllNotification

from django.conf import settings 
from django.conf.urls.static import static
from application.views import mypdf, applicationDetail, registrationview

# router.register('enquiry',views.enquiryViewset, basename="enquiry")

# router1.register('application',views.applicationViewset, basename="application")


urlpatterns = [path("select2/", include("django_select2.urls")),

# Notification URLS 
# path('notification/',notification, name='notification' ),
# path('inbox/notifications/',include(notifications.urls, namespace='Notifications')),
# path('notification/allnotification/',seeAllNotification, name = "see-all-notification"),
# path('notification/mark-read/<int:pk>', markRead, name='mark-read'),

# path("api/",include(router.urls)),
# path("api/",include(router1.urls)),
# API ROUTES

# REACT ROUTES
path("",front, name="front"),
path("login",front),
path("enquiries", front),
path("enquiry/create", front),
path("applications", front),
path("application/create", front),
path("user-profile",front),
# ====================

path('api/', include('api.urls')),


path('course-autocomplete/',CourseAutocomplete.as_view(), name='course-autocomplete'),
path('pdf/<int:pk>/', mypdf, name='pdf'),
path('comment/', include('comment.urls')),
path('enquirydetail/<int:pk>/', enquiryview, name = 'enquiry-detail'),
path('applicationdetail/<int:pk>/',applicationDetail, name= 'application-detail'),
path('registration/', registrationview, name='registration'),
path("auth/", include("rest_framework.urls", namespace='rest_framework')),
path('admin/',admin.site.urls, name='adminSite'),

path("login.html", TemplateView.as_view(template_name="login.html"), name="login"),
path("index.html", TemplateView.as_view(template_name="index.html"), name="index"),
path("view_uni.html",TemplateView.as_view(template_name="view_uni.html"),name="view_uni",),
path("view_application.html",TemplateView.as_view(template_name="view_application.html"),name="view_application",),

path("user.html", TemplateView.as_view(template_name="user.html"), name="user"),

path("user_type.html",TemplateView.as_view(template_name="user_type.html"),name="user_type",),

path("update_field.html",TemplateView.as_view(template_name="update_field.html"),name="update_field",),

path("university.html",TemplateView.as_view(template_name="university.html"),name="university",),

path("edit_user_type.html",TemplateView.as_view(template_name="edit_user_type.html"),name="edit_user_type",),
path("edit_university.html",TemplateView.as_view(template_name="edit_university.html"),name="edit_university",),
path("edit_enquiry.html",TemplateView.as_view(template_name="edit_enquiry.html"),name="edit_enquiry",),
path("edit_appication_status.html",TemplateView.as_view(template_name="edit_appication_status.html"),name="edit_appication_status",),
path("courses.html/", TemplateView.as_view(template_name="courses.html"), name="courses"),
path("applications.html",TemplateView.as_view(template_name="applications.html"),name="applications",),
path("application_status.html",TemplateView.as_view(template_name="application_status.html"),name="application_status",),
path("app-profile.html",TemplateView.as_view(template_name="app-profile.html"),name="app-profile",),
path("announcement.html",TemplateView.as_view(template_name="announcement.html"),name="announcement",),
path("add_user.html",TemplateView.as_view(template_name="add_user.html"),name="add_user",),
path("add_user_type.html",TemplateView.as_view(template_name="add_user_type.html"),name="add_user_type",),
path("add_university.html",TemplateView.as_view(template_name="add_university.html"),name="add_university",),
path("add_enquiry.html",TemplateView.as_view(template_name="add_enquiry.html"),name="add_enquiry",),
path("add_courses.html",TemplateView.as_view(template_name="add_courses.html"),name="add_courses",),
path("add_application.html",TemplateView.as_view(template_name="add_application.html"),name="add_application"),
path("add_application_status.html",TemplateView.as_view(template_name="add_application_status.html"),name="add_application_status",),
path("enquiry.html",TemplateView.as_view(template_name="enquiry.html")),
]


admin.site.site_header = "FLYURDREAM CRM"
admin.site.site_title = "FLYURDREAM CRM"
admin.site.index_title = "FLYURDREAM CRM"


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 