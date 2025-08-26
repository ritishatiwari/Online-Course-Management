from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from adminapp.models import course,batch
import datetime
from . import models
from coursemanagement.models import mstuser
from django.http import HttpResponse
from django.contrib.auth import logout

# from django.contrib import messages


def sessioncheckstudent_middleware(get_response):
 def middleware(request):
    if request.path=='/studenthome/'or request.path=='/studenthome/admission/' or request.path=='/studenthome/batchlist2/' or request.path=='/studenthome/courselist2/' or request.path=='/studenthome/success/' or request.path=='/studenthome/updateprofile/':
      if "emailid" not in request.session:  
            response=redirect('/login/')
      else:
            response=get_response(request)
    else:
        response=get_response(request)
    return response
 return middleware 

# Create your views here.
def studenthome(request):
    #for fetch session-------------------------------------
    emailid=request.session.get("emailid")
    role=request.session.get("role")
    #------------------------------------------------------
    return render(request,"studenthome.html",
        {"emailid":emailid,"role":role})


def courselist2(request):
    result=course.objects.all()
    return render(request,"courselist2.html",{"result":result})

def batchlist2(request):
    result=batch.objects.filter(batchstatus=1)
    return render (request,"batchlist2.html",
                   {"result":result})

# from .models import Batch, Admission  # Use your actual model names
    
def admission(request):
   
    if request.method=="GET":
        batchid=request.GET.get("batchid")
        # print("batchid -",batchid)
        res = batch.objects.filter(batchid=batchid)
        return render(request,"admission.html",{"res":res})
    else:  # POST
        batchid = request.POST.get("batchid")
        emailid = request.session.get("emailid")

        x = datetime.datetime.now()
        admissiondate = x.strftime("%Y-%m-%d")

        res = models.admission(batchid=batchid, emailid=emailid, admissiondate=admissiondate)
        res.save()
        
        return redirect("/studenthome/success/")


def success(request):
    return render(request,"success.html")

def updateprofile(request):
 if request.method=="GET":
   emailid=request.session.get("emailid")
   res=mstuser.objects.filter(emailid=emailid)
   return render(request,"updateprofile.html",{"res":res})
 else:
   name=request.POST.get("name")
   mobile=request.POST.get("mobile")
   address=request.POST.get("address")
   city=request.POST.get("city")
   gender=request.POST.get("gender")
   pwd=request.POST.get("pwd")
   emailid=request.POST.get("emailid")
   obj=mstuser.objects.filter(emailid=emailid).update(name=name,mobile=mobile,address=address,pwd=pwd,city=city,gender=gender)
  
   return redirect("/studenthome/")  
 
def studentlogout(request):
   logout(request)
   return redirect("http://localhost:8000")

