from apps.courses.models import Category

def global_context(request):
    return {
        'site_name': 'Arshith Springboard Enterprise',
        'site_tagline': 'Digital Learning Platform inspired by Infosys Springboard',
        'nav_categories': Category.objects.all()[:8]
    }
