from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DiaryEntry, Tag
from .forms import DiaryEntryForm

@login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='/login/')
def page(request):
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=True, user=request.user)
            messages.success(request, f'Diary entry "{entry.title}" created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DiaryEntryForm()
    return render(request, 'page.html', {'form': form})
