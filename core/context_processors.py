from .models import SiteSetting

def site_settings(request):
    """Provides dynamic logo and title to all templates."""
    setting = SiteSetting.objects.first()
    return {'site_settings': setting}