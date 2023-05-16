from django.shortcuts import render
from .models import Application
from django.views.generic import TemplateView
from enquiry.models import enquiry

from django.shortcuts import  render, redirect

from django.contrib.auth import login
from django.contrib import messages
from .forms import UserForm

class mypdf(TemplateView):
    # filename = 'download.pdf'
    template_name = 'pdf/pdf.html'

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context["q"] =  Application.objects.all()
        return context
    

def mypdf(request,pk):
    q = Application.objects.get(id=pk)
    enquiry_obj = enquiry.objects.get(id=q.name.id)
    return render(request, 'pdf/pdf.html', context={'i':q, 'enquiry_obj':enquiry_obj})


def applicationDetail(request, pk):
    context ={'obj':Application.objects.get(id=pk)}
    
    return render(request, 'comments.html', context=context)


def registrationview(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # msg = messages.success(request, "Registration Successful")
            return redirect('/')

        
        else:
            print(form.errors)
            return render(request, 'registration.html',{'form':form} )

    
    else:
        form = UserForm()
    return render(request, "registration.html", context={"form":form})


        