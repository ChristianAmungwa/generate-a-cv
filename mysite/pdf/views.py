from django.shortcuts import render
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io


# Create your views    here.

def accept(request):
    if request.method == "POST":
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        phone = request.POST.get("phone","")
        summary = request.POST.get("summary","")
        degree = request.POST.get("degree","")
        school = request.POST.get("school","")
        university = request.POST.get("university","")
        previous_work= request.POST.get("previous_work","")
        skills = request.POST.get("skills","")

        profile = Profile(name=name,email=email,phone=phone,summary=summary,degree=degree,school=school,university=university,previous_work=previous_work,skills=skills)
        profile.save() # this saves any entered data into the backend database
# "profile" above is an object of the class model "Profile", which os found in models.py        .
#Testing
    
    return render(request,'pdf/accept.html')


#def resume(request,id):
    #user_profile = Profile.objects.get(pk=id)
    #return render(request,'pdf/resume.html',{'user_profile':user_profile})

# "{'user_profile':user_profile}" is a python dictionary that represents a key:value


def resume(request,id): # "id" here is necessary because each time you download a profile, you only want to download the cv of a specific person with a specific id, instead of downloading every single profile each time.

    user_profile = Profile.objects.get(pk=id) # "pk" here refers to "primary keyword"
    template = loader.get_template('pdf/resume.html')
    html = template.render({'user_profile':user_profile})

    options ={
        'page-size':'Letter',
        'encoding':"UTF-8",
    }
    #SET TO UR PATH


    config = pdfkit.configuration(wkhtmltopdf=r'C:\Users\alexd\Downloads\wkhtmltox-0.12.6-1.msvc2015-win64\bin\wkhtmltopdf.exe')

    #Must be 'option=options' and add 'configuration=config'
    pdf = pdfkit.from_string(html,False,options=options,configuration=config)
    response = HttpResponse(pdf,content_type='application/pdf')
 
    #filename must be included in contentdisposition
    response['Content-Disposition'] ='attachment;filename=resume.pdf'
 
    return response



def list(request):
    profiles = Profile.objects.all()
    return render(request,'pdf/list.html',{'profiles':profiles})
