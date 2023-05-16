from django.urls import include, path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('applications',applicationViewset, basename='application')
router.register('enquiries',enquiryViewset, basename='enquiry')
router.register('courses',courseViewset, basename='course')
router.register('universities',UniversityViewset, basename='university')

urlpatterns = [
        path("enq/postcomment/",EnquiryCommentCreateView.as_view()),
        path("enq/getcomment/", EnquiryCommentView.as_view(), name="comment"),
        path("recent-actions", recentactions_view.as_view()),
        path("broadcast-message", Broadcast_view.as_view(), name = 'broadcast'),

        path('filter-university/', University_requirement_view.as_view(), name = 'filter-enquiry'),

    path('add-enquiry/',add_enquiry.as_view(), name='add-enquiry'),
    path('update-enquiry/<int:pk>/', update_enquiry.as_view(), name = 'update-enquiry'),
        # application endpoints
    path('add-application/', add_application.as_view(), name='add-application'),
    path('update-application/<int:pk>/',update_application.as_view(), name='update-application'),
    path('view-enquiry/',enquiry_view().as_view(), name="view-enquiry"),

    path("courseslists/", course_view_only.as_view(), name='courseslists'),
    path("universitieslists/", university_view.as_view(), name="universities"),
    path("countries/", countryview.as_view(), name='countries'),
    path("courselevels/", course_level_view.as_view(), name='courselevels'),
    path("currenteducation/", current_education_view.as_view(), name='currenteducation'),
    path("enquirystatus/", enquiry_status_view.as_view(), name='enquirystatus'),
    path("intakes/", intakeView.as_view(), name='intakes'),
    path("userlist/", assigned_user_view.as_view(), name="userlist"),
    path("appstatus/",application_status_view.as_view(),name = "appstatus"),
    
    path("user/login/", LoginView.as_view(), name='loginview'),
    path('user/profile/', ProfileView.as_view(), name='profileview'),
    path('user/changepassword/', ChangePasswordView.as_view(), name='change-password'),
    path('user/resetpassword/', SendPasswordResetView.as_view(), name='reset-password'),
    path('user/resetpassword/<uid>/<token>/', PasswordResetView.as_view(), name="reset-with-link"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('', include(router.urls), name='see-enquiry'),
    path('enquirydata/', new_enquiry_view.as_view(),),
    path('applicationdata/', new_application_view.as_view(),),
    
    # path('user/notifications/', NotificationView.as_view()),
    # path('user/notifications/<int:pk>/', NotificationMarkReadView.as_view()),

    
    # path('enquiry/<int:pk>', ListEnquiry.as_view(), name='see-enquiry'),

    
    

]


