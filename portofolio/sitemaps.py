from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class PortfolioSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'

    def get_urls(self, page=1, site=None, protocol=None, **kwargs):
        return super().get_urls(page=page, site=site, protocol='https', **kwargs)

    def items(self):
        return ('home', 'experience', 'profile')

    def location(self, item):
        return reverse(f'portofolio:{item}')


portfolio_sitemaps = {'portfolio': PortfolioSitemap}