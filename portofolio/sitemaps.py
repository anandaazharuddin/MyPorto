from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class PortfolioSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return ('home', 'experience', 'profile')

    def location(self, item):
        return reverse(f'portofolio:{item}')


portfolio_sitemaps = {'portfolio': PortfolioSitemap}