from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from .models import Document
from .forms import DocumentForm
from .chat import assistant

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

@login_required
@require_http_methods(["POST"])
def chat(request):
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        message = data.get('message')
        document_id = data.get('document_id')

        # Verify document ownership and get the actual file path
        document = get_object_or_404(Document, id=document_id, user=request.user)
        document_path = document.file.path  # Get the actual file system path

        # Process the message using our ChatAssistant
        response = assistant.process_message(message, document_path)

        return JsonResponse({
            'status': 'success',
            'response': response
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data'
        }, status=400)
    except Document.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Document not found or access denied'
        }, status=404)
    except Exception as e:
        print(f"Chat error: {str(e)}")  # Add logging for debugging
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
