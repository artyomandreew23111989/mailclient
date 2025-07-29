from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ComposeForm, ContactForm
from .models import Message, Folder, Contact

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def inbox(request):
    # Правильный запрос с использованием request.user
    folders = Folder.objects.filter(user=request.user)
    return render(request, 'mailapp/inbox.html', {'folders': folders})

@login_required
def compose(request):
    if request.method == 'POST':
        form = ComposeForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.email
            message.save()
            return redirect('inbox')
    else:
        form = ComposeForm()
    return render(request, 'mailapp/compose.html',)