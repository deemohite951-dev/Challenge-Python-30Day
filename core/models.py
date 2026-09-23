from django.db import models
from django.contrib.auth.models import User

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, default="SocialSolve")
    site_logo = models.ImageField(upload_to="logos/", blank=True, null=True, help_text="Upload brand logo for navbar")
    homepage_bg = models.ImageField(upload_to="site_bg/", blank=True, null=True, help_text="Dashboard background image")

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return f"{self.site_name} Configuration"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class IssueReport(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="issues")
    
    # Step 1: Core Details
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    # Step 2: Location & Incident Time
    location = models.CharField(max_length=255)
    incident_date = models.DateField()
    incident_time = models.TimeField()

    # Step 3: Photo (Can be skipped)
    photo = models.ImageField(upload_to="issue_photos/", blank=True, null=True)

    # Workflow & Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title}"