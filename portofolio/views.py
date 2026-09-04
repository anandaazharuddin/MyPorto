from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactForm
from .models import (Certification, Education, Experience, Language,
                     Organization, Profile, Project, Tag)
from .models import Skill


def home(request):
    selected_tag = request.GET.get('tag', '')
    projects = Project.objects.filter(is_featured=True).prefetch_related('tags', 'gallery')
    if selected_tag:
        projects = projects.filter(tags__name__iexact=selected_tag)

    profile = Profile.objects.prefetch_related('gallery').first()
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Thanks for reaching out. I will get back to you soon.')
        return redirect('portofolio:home')

    return render(request, 'portofolio/home.html', {
        'projects': projects[:6],
        'profile': profile,
        'tags': Tag.objects.all(),
        'experiences': Experience.objects.all(),
        'educations': Education.objects.all(),
        'certifications': Certification.objects.all(),
        'languages': Language.objects.all(),
        'organizations': Organization.objects.all(),
        'form': form,
        'selected_tag': selected_tag,
        'skills': Skill.objects.all(),
    })


def experience_page(request):
    return render(request, 'portofolio/experience.html', {
        'profile': Profile.objects.first(),
        'experiences': Experience.objects.prefetch_related('gallery'),
        'educations': Education.objects.all(),
    })


def profile_page(request):
    return render(request, 'portofolio/profile.html', {
        'profile': Profile.objects.first(),
        'educations': Education.objects.all(),
        'certifications': Certification.objects.all(),
        'languages': Language.objects.all(),
        'organizations': Organization.objects.all(),
    })