from django.shortcuts import render, get_object_or_404
from .models import Project
from core.models import Category, Tag
from django.db.models import Q

def project_list(request):
    projects = Project.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    category_filter = request.GET.get('category')
    tag_filter = request.GET.get('tag')
    search_query = request.GET.get('q', '')

    if category_filter:
        projects = projects.filter(category__slug__iexact=category_filter)

    if tag_filter:
        projects = projects.filter(tags__slug__iexact=tag_filter)
    
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    context = {
        'projects': projects,
        'categories': categories,
        'tags': tags,
        'active_category': category_filter,
        'active_tag': tag_filter,
        'search_query': search_query,
    }
    return render(request, 'projects/project_list.html', context)

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})
