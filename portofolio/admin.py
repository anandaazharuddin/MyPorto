from django.contrib import admin
from django.utils.html import format_html
from .models import (Certification, Education, Experience, ExperienceImage,
                     Language, Message, Organization, Project, ProjectImage,
                     Profile, ProfileImage, Tag)
from .models import Skill


class RestrictedAdminSite(admin.AdminSite):
    site_header = 'Portfolio administration'
    site_title = 'Portfolio administration'
    index_title = 'Portfolio administration'

    def has_permission(self, request):
        user = request.user
        return user.is_active and user.is_staff and user.is_superuser

    def index(self, request, extra_context=None):
        """Dashboard index with quick stats for the control panel."""
        stats = {
            'projects': Project.objects.count(),
            'featured': Project.objects.filter(is_featured=True).count(),
            'messages': Message.objects.count(),
            'unread': Message.objects.filter(is_read=False).count(),
            'experiences': Experience.objects.count(),
            'certifications': Certification.objects.count(),
        }
        context = {'stats': stats}
        context.update(extra_context or {})
        return super().index(request, extra_context=context)


admin_site = RestrictedAdminSite(name='secure_admin')


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


@admin.register(Skill, site=admin_site)
class SkillAdmin(GlassAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    search_fields = ('name',)
    ordering = ('order', 'name')


@admin.register(Project, site=admin_site)
class ProjectAdmin(GlassAdmin):
    list_display = ('title', 'featured_flag', 'is_featured', 'order', 'created_at')
    list_display_links = ('title',)
    list_filter = ('is_featured', 'tags', 'created_at')
    search_fields = ('title', 'description', 'tags__name')
    filter_horizontal = ('tags',)
    inlines = (ProjectImageInline,)
    readonly_fields = ('created_at',)
    save_on_top = True
    actions = ('make_featured', 'unmake_featured')
    fieldsets = (
        (None, {'fields': ('title', 'description', 'image')}),
        ('Links', {'fields': ('url', 'github_url')}),
        ('Visibility & ordering', {'fields': ('is_featured', 'tags', 'order')}),
        ('Meta', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )

    @admin.display(description='Featured')
    def featured_flag(self, obj):
        if obj.is_featured:
            return format_html('<span class="star" title="Featured project">&#9733;</span>')
        return format_html('<span class="star star-off" title="Not featured">&#9734;</span>')

    @admin.action(description='Mark selected projects as featured')
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} project(s) marked as featured.')

    @admin.action(description='Remove featured flag from selected projects')
    def unmake_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'Featured flag removed from {updated} project(s).')


@admin.register(Profile, site=admin_site)
class ProfileAdmin(GlassAdmin):
    list_display = ('name', 'email')
    inlines = (ProfileImageInline,)
    save_on_top = True
    fieldsets = (
        ('Identity', {'fields': ('name', 'headline', 'subheadline', 'bio', 'avatar', 'cv_file')}),
        ('Contact & social links', {'fields': ('email', 'github', 'linkedin', 'instagram', 'twitter', 'tiktok')}),
    )


@admin.register(Tag, site=admin_site)
class TagAdmin(GlassAdmin):
    search_fields = ('name',)


@admin.register(Experience, site=admin_site)
class ExperienceAdmin(GlassAdmin):
    list_display = ('role', 'company', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current',)
    search_fields = ('company', 'role')
    inlines = (ExperienceImageInline,)
    save_on_top = True
    fieldsets = (
        (None, {'fields': ('company', 'role', 'description')}),
        ('Dates', {'fields': ('start_date', 'end_date', 'is_current')}),
    )


@admin.register(Education, site=admin_site)
class EducationAdmin(GlassAdmin):
    list_display = ('institution', 'degree', 'field', 'year', 'score')
    search_fields = ('institution', 'degree', 'field')


@admin.register(Certification, site=admin_site)
class CertificationAdmin(GlassAdmin):
    list_display = ('name', 'issuing_organization', 'issue_date', 'credential_id')
    search_fields = ('name', 'issuing_organization', 'credential_id')
    list_filter = ('issuing_organization',)
    date_hierarchy = 'issue_date'
    fieldsets = (
        (None, {'fields': ('name', 'issuing_organization', 'image')}),
        ('Credential details', {'fields': ('issue_date', 'expiration_date', 'credential_id', 'credential_url', 'description')}),
    )


@admin.register(Language, site=admin_site)
class LanguageAdmin(GlassAdmin):
    list_display = ('name', 'proficiency')
    list_filter = ('proficiency',)


@admin.register(Organization, site=admin_site)
class OrganizationAdmin(GlassAdmin):
    list_display = ('name', 'role', 'start_date', 'end_date')
    search_fields = ('name', 'role', 'description')
    fieldsets = (
        (None, {'fields': ('name', 'role', 'url', 'image')}),
        ('Membership', {'fields': ('start_date', 'end_date', 'description')}),
    )


@admin.register(Message, site=admin_site)
class MessageAdmin(GlassAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    actions = ('mark_as_read', 'mark_as_unread')

    @admin.action(description='Mark selected messages as read')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description='Mark selected messages as unread')
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
