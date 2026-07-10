from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import DiaryEntry, Tag

@login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='/login/')
def page(request):
    return render(request, 'page.html')
