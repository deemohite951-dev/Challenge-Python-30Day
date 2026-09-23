from django.contrib import admin
from .models import SiteSetting, Category, IssueReport

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'site_logo', 'homepage_bg')

    def has_add_permission(self, request):
        # Keep singleton pattern: only one instance allowed
        return not SiteSetting.objects.exists()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(IssueReport)
class IssueReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'reporter', 'category', 'status', 'incident_date', 'created_at')
    list_filter = ('status', 'category', 'incident_date')
    search_fields = ('title', 'description', 'location')
    list_editable = ('status',)