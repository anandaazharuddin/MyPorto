from django.contrib import admin
from .models import (Certification, Education, Experience, ExperienceImage,
                     Language, Message, Organization, Project, ProjectImage,
                     Profile, ProfileImage, Tag)


class ProjectImageInline(admin.StackedInline):
    model = ProjectImage
    extra = 1
    fields = ('image', 'description', 'order')


class ExperienceImageInline(admin.StackedInline):
    model = ExperienceImage
    extra = 1
    fields = ('image', 'description', 'order')


class ProfileImageInline(admin.StackedInline):
    model = ProfileImage
    extra = 1
    fields = ('image', 'description', 'order')


class GlassAdmin(admin.ModelAdmin):
    class Media:
        css = {'all': ('css/admin-glass.css',)}

@admin.register(Project)
class ProjectAdmin(GlassAdmin):
    list_display = ('title', 'is_featured', 'order', 'created_at')
    list_filter = ('is_featured', 'tags')
    search_fields = ('title', 'description')
    filter_horizontal = ('tags',)
    inlines = (ProjectImageInline,)

@admin.register(Profile)
class ProfileAdmin(GlassAdmin):
    list_display = ('name', 'email')
    inlines = (ProfileImageInline,)
    fieldsets = (
        ('Identity', {'fields': ('name', 'headline', 'subheadline', 'bio', 'avatar', 'cv_file')}),
        ('Contact & social links', {'fields': ('email', 'github', 'linkedin', 'instagram', 'twitter', 'tiktok')}),
    )

@admin.register(Tag)
class TagAdmin(GlassAdmin):
    search_fields = ('name',)


@admin.register(Experience)
class ExperienceAdmin(GlassAdmin):
    list_display = ('role', 'company', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current',)
    search_fields = ('company', 'role')
    inlines = (ExperienceImageInline,)


@admin.register(Education)
class EducationAdmin(GlassAdmin):
    list_display = ('institution', 'degree', 'field', 'year', 'score')
    search_fields = ('institution', 'degree', 'field')


@admin.register(Certification)
class CertificationAdmin(GlassAdmin):
    list_display = ('name', 'issuing_organization', 'issue_date', 'credential_id')
    search_fields = ('name', 'issuing_organization', 'credential_id')
    list_filter = ('issuing_organization',)


@admin.register(Language)
class LanguageAdmin(GlassAdmin):
    list_display = ('name', 'proficiency')
    list_filter = ('proficiency',)


@admin.register(Organization)
class OrganizationAdmin(GlassAdmin):
    list_display = ('name', 'role', 'start_date', 'end_date')
    search_fields = ('name', 'role', 'description')


@admin.register(Message)
class MessageAdmin(GlassAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'subject', 'message')
    actions = ('mark_as_read', 'mark_as_unread')

    @admin.action(description='Mark selected messages as read')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description='Mark selected messages as unread')
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)