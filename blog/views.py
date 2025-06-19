from django.shortcuts import render, get_object_or_404
from .models import BlogPost
from core.models import Category, Tag
from django.db.models import Q

def blog_list(request):
    posts = BlogPost.objects.all().order_by('-published_date')
    categories = Category.objects.all()
    tags = Tag.objects.all()

    category_filter = request.GET.get('category')
    tag_filter = request.GET.get('tag')
    search_query = request.GET.get('q', '')

    if category_filter:
        posts = posts.filter(category__slug__iexact=category_filter)

    if tag_filter:
        posts = posts.filter(tags__slug__iexact=tag_filter)

    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query)
        )

    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'active_category': category_filter,
        'active_tag': tag_filter,
        'search_query': search_query,
    }
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/blog_detail.html', {'post': post})
