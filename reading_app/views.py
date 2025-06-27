from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Document
from .forms import DocumentForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'reading_app/register.html', {'form': form})

@login_required
def home(request):
    documents = Document.objects.filter(user=request.user)
    return render(request, 'reading_app/home.html', {'documents': documents})

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'reading_app/upload.html', {'form': form})

@login_required
def view_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, user=request.user)
    return render(request, 'reading_app/view_document.html', {'document': document})
