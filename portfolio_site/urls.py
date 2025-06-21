"""
URL configuration for portfolio_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps import GenericSitemap
from django.http import HttpResponse
from django.template.loader import render_to_string
from projects.models import Project
from blog.models import BlogPost
from django.contrib.sitemaps.views import sitemap

# Sitemap configuration
sitemaps = {
    'projects': GenericSitemap({
        'queryset': Project.objects.all(),
        'date_field': 'id',
    }, priority=0.6),
    'blog': GenericSitemap({
        'queryset': BlogPost.objects.all(),
        'date_field': 'published_date',
    }, priority=0.5),
}

def robots_txt(request):
    content = render_to_string('robots.txt', {
        'sitemap_url': request.build_absolute_uri('/sitemap.xml')
    })
    return HttpResponse(content, content_type='text/plain')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('', include('home.urls')),
    path('projects/', include('projects.urls')),
    path('blog/', include('blog.urls')),
    path('contact/', include('contact.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

