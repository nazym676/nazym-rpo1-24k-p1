from django.db.models.functions import Lower
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import request
from .models import Category,Post, Adv
from django.db.models import Q

def home_page(request):
    hot_posts = Post.objects.all().order_by('-created_at')[:4]
    posts = Post.objects.all().order_by('-created_at')[:5]
    advs = Adv.objects.all()[:4]
    context = {
        'hot_posts':hot_posts,
        'posts':posts,
        'advs':advs
    }
    return render(request, "index.html", context)

def all_news_page(request):
    posts = Post.objects.all().order_by('-created_at')
    advs = Adv.objects.all()[:4]
    context = {
        'posts':posts,
        'advs':advs
    }
    return render(request, "all-news.html", context)

def news_by_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=category).order_by('-created_at')
    advs = Adv.objects.all()[:4]
    context = {
        'category':category,
        'posts':posts,
        'advs':advs
    }
    return render(request, "news-by-category.html", context)

def search_page(request):
    return render(request, "search.html")

def search_results(request):
    query = request.GET.get('q')
    advs = Adv.objects.all()[:4]
    results = []
    if query:
        results = Post.objects.annotate(
            title_lower=Lower('title'),
            description_lower=Lower('description')
        ).filter(
            Q(title_lower__icontains=query.lower()) | Q(description_lower__icontains=query.lower())
        )
    context = {
        'query':query,
        'results':results,
        'advs':advs
    }
    return render(request, "search-result.html", context)

def read_news_page(request, pk):
    post = get_object_or_404(Post, pk=pk)
    advs = Adv.objects.all()[:4]

    related_posts = Post.objects.filter(
        category=post.category
    ).exclude(
        pk=post.pk
    ).order_by('-created_at')[:4]

    context = {
        'post':post,
        'advs':advs,
        'related_posts':related_posts
    }
    return render(request, "read-news.html", context)