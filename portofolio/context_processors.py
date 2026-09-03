from django.conf import settings


def site_metadata(request):
    return {'SITE_URL': settings.SITE_URL}