from django.shortcuts import render
from django.contrib import messages
from portfolio import models
from .models import Post  # Make sure this model exists
from django.shortcuts import get_object_or_404



def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def skills(request):
    return render(request, 'skills.html')

def blog(request):
    posts = Post.objects.all().order_by('-created_at')  # Or whatever field you use
    return render(request, 'blog.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

def projects(request):
    return render(request, 'projects.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        number = request.POST.get('number')

        # Validation
        if not (1 < len(name) < 30):
            messages.error(request, 'Length of name should be between 2 and 30 characters')
            return render(request, 'contact.html')

        if not (1 < len(email) < 30):
            messages.error(request, 'Length of email should be between 2 and 30 characters')
            return render(request, 'contact.html')

        if not (1 < len(number) < 14):
            messages.error(request, 'Phone number should be between 2 and 14 characters')
            return render(request, 'contact.html')

        # Save to database
        ins = models.Contact(name=name, email=email, content=content, number=number)
        ins.save()
        messages.success(request, 'Thank you for contacting me')

    return render(request, 'contact.html')
