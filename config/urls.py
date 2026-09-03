from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import include, path

from portofolio.sitemaps import portfolio_sitemaps


def robots_txt(request):
    return HttpResponse(
        'User-agent: *\nAllow: /\n\nSitemap: https://anandaazharuddin.site/sitemap.xml\n',
        content_type='text/plain',
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': portfolio_sitemaps}, name='sitemap'),
    path('robots.txt', robots_txt, name='robots'),
    path('', include('portofolio.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)