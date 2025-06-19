from django.db import models
from core.models import Category, Tag

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(help_text="A short summary of the project.")
    detailed_description = models.TextField(blank=True, help_text="A more detailed description of the project, can include challenges, features, etc.")
    technology = models.CharField(max_length=100)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True, help_text="The main thumbnail image for the project.")
    live_demo_link = models.URLField(blank=True, null=True, help_text="A link to the live demo of the project.")
    link = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']

class ProjectScreenshot(models.Model):
    project = models.ForeignKey(Project, related_name='screenshots', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_screenshots/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Screenshot for {self.project.title}"

# Create your models here.
