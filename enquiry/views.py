from django.shortcuts import render
from django.urls import reverse
# from notifications.models import Notification
from .models import enquiry, Course
# Create your views here.
from django.db.models import Q
from django.shortcuts import redirect

# def notification(request):
#     qs = Notification.objects.all()
#     qs1 = qs.filter(recipient=request.user)
#     qs = qs1.unread()
#     print(qs.count())
#     return render(request, "admin/notify.html/", {'qs': qs})

def front(request):
    context = {}
    return render(request, 'index.html', context)



# def markRead(request,pk):
#     qs = Notification.objects.all()
#     qs1 = qs.filter(recipient=request.user)
#     qs = qs1.unread()
#     obj = qs.filter(recipient=request.user)
#     obj = obj.get(id=pk)
#     obj.mark_as_read()
#     return redirect('notification')
    
# def seeAllNotification(request):
#     qs = Notification.objects.all()
#     qs1 = qs.filter(recipient=request.user)
#     user = request.user
#     return render(request,"admin/allnotification.html", {"notifications": qs1, "user":user})


from dal import autocomplete


class CourseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Course.objects.none()

        qs = Course.objects.all()

        if self.q:
            qs = qs.filter(course_name__istartswith=self.q)

        return qs


class CourseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Course.objects.none()

        qs = Course.objects.all()

        course = self.forwarded.get('university_interested', None)
        coursetype =  self.forwarded.get('level_applying_for', None)
        # print('**********'+course+'**************')
        # print(coursetype)
        # print('**********'+coursetype+'**************')
        
        if course and coursetype:

            qs = qs.filter(Q(university=course) & Q(course_levels=coursetype)).filter(Active=True)

        if self.q:

            qs = None
        return qs
        
        
        
        
def enquiryview(request,pk):
    context ={
        'obj':enquiry.objects.get(id=pk)
    }
    return render(request,'comments.html', context = context)
