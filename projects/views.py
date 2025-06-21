from django.shortcuts import render, get_object_or_404
from .models import Project
from core.models import Category, Tag
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@cache_page(300)  # Cache for 5 minutes
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

    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(projects, 6)  # 6 projects per page
    page_obj = paginator.get_page(page_number)

    context = {
        'projects': page_obj.object_list,
        'categories': categories,
        'tags': tags,
        'active_category': category_filter,
        'active_tag': tag_filter,
        'search_query': search_query,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('projects/_project_cards.html', context, request=request)
        return JsonResponse({
            'html': html,
            'has_next': page_obj.has_next(),
        })

    return render(request, 'projects/project_list.html', context)

@cache_page(300)  # Cache for 5 minutes
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})
