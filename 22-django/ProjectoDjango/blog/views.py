from django.shortcuts import render
from blog.models import Category, Article
# Create your views here.

def list(request):

    return render(request, 'articles/list.html', {
        'title': 'Artículos',
        'title': articles,
    })