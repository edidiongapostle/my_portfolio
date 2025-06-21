from django.db import models
from core.models import Category, Tag
from PIL import Image
import os

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

    def save(self, *args, **kwargs):
        # Call the parent save method first
        super().save(*args, **kwargs)
        
        # Optimize image if it exists
        if self.image:
            self.optimize_image()

    def optimize_image(self):
        """Optimize the uploaded image by resizing and compressing it."""
        if self.image:
            try:
                img = Image.open(self.image.path)
                
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if too large (max 800x600)
                if img.width > 800 or img.height > 600:
                    img.thumbnail((800, 600), Image.Resampling.LANCZOS)
                
                # Save optimized image
                img.save(self.image.path, 'JPEG', quality=85, optimize=True)
            except Exception as e:
                print(f"Error optimizing image for project {self.title}: {e}")

    def get_thumbnail_url(self):
        """Get a smaller version of the image for thumbnails."""
        if self.image:
            return self.image.url
        return None

    class Meta:
        ordering = ['id']

class ProjectScreenshot(models.Model):
    project = models.ForeignKey(Project, related_name='screenshots', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_screenshots/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Screenshot for {self.project.title}"

# Create your models here.
