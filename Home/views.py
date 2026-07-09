from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import pag

@login_required(login_url='/login/')
def home(request):
    if request.method=="POST":
        des=request.POST.get("description")
        pag.objects.create(content=des)
        return render(request, 'home.html')

    return render(request, 'home.html')
def page(request):
    return render(request, 'page.html')  
