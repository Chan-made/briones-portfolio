from django.contrib import admin
from django.utils.html import format_html
from django.utils.timezone import localtime
from .models import (
    Profile, About, ContactInfo, ContactMessage,
    Project, Education, Skill, Owner,
)


# ─────────────────────────────────────────────
#  PROFILE
# ─────────────────────────────────────────────

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identity', {
            'fields': ('full_name', 'tagline', 'profile_photo'),
        }),
    )
    readonly_fields  = ('photo_preview',)
    list_display     = ('full_name', 'tagline', 'photo_preview')
    list_display_links = ('full_name',)

    def photo_preview(self, obj):
        if obj.profile_photo:
            return format_html(
                '<img src="{}" style="height:48px;width:48px;object-fit:cover;'
                'border-radius:50%;border:2px solid #FFE600;" />',
                obj.profile_photo.url,
            )
        return format_html('<span style="color:#888;">No photo</span>')
    photo_preview.short_description = 'Photo'

    def has_add_permission(self, request):
        return not Profile.objects.exists()


# ─────────────────────────────────────────────
#  ABOUT
# ─────────────────────────────────────────────

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Bio', {
            'fields': ('short_bio', 'full_bio'),
            'description': (
                '<strong>Tip:</strong> Separate full_bio paragraphs with a blank line '
                'so they render as separate &lt;p&gt; tags in the template.'
            ),
        }),
        ('Career Goals', {
            'fields': ('career_goals',),
        }),
    )
    readonly_fields = ()
    list_display    = ('__str__',) 
    
    def has_add_permission(self, request):
        return not About.objects.exists()


# ─────────────────────────────────────────────
#  CONTACT INFO  (singleton)
# ─────────────────────────────────────────────

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Primary Contact', {
            'fields': ('email', 'phone'),
        }),
        ('Social Links', {
            'fields': ('github_url', 'linkedin_url', 'twitter_url', 'facebook_url', 'instagram_url'),
            'classes': ('collapse',),
        }),
        ('Contact Page Note', {
            'fields': ('contact_note',),
        }),
    )
    # Check if updated_at exists in your ContactInfo model
    readonly_fields = ()  # Removed 'updated_at'
    list_display    = ('email', 'phone')  # Removed 'updated_at'

    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()


# ─────────────────────────────────────────────
#  CONTACT MESSAGES  (incoming)
# ─────────────────────────────────────────────

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'subject', 'short_message', 'status_badge', 'sent_at_local')
    list_filter   = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Message', {
            'fields': ('name', 'email', 'subject', 'message', 'created_at'),
        }),
        ('Admin', {
            'fields': ('status', 'admin_notes'),
        }),
    )

    def short_message(self, obj):
        return obj.message[:60] + '…' if len(obj.message) > 60 else obj.message
    short_message.short_description = 'Message'

    def status_badge(self, obj):
        colors = {
            'new':      ('#FFE600', '#111'),
            'read':     ('#444',    '#eee'),
            'replied':  ('#00c864', '#111'),
            'archived': ('#333',    '#888'),
        }
        bg, fg = colors.get(obj.status, ('#555', '#fff'))
        return format_html(
            '<span style="background:{};color:{};padding:2px 10px;border-radius:12px;'
            'font-size:0.72rem;font-weight:700;letter-spacing:1px;">{}</span>',
            bg, fg, obj.get_status_display().upper(),
        )
    status_badge.short_description = 'Status'

    def sent_at_local(self, obj):
        return localtime(obj.created_at).strftime('%b %d, %Y  %H:%M')
    sent_at_local.short_description = 'Received'
    sent_at_local.admin_order_field = 'created_at'


# ─────────────────────────────────────────────
#  PROJECT
# ─────────────────────────────────────────────

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display        = ('title', 'tools_preview', 'github_link', 'order', 'created_at')
    list_display_links  = ('title',)
    list_editable       = ('order',)
    search_fields       = ('title', 'description', 'tools')
    ordering            = ('order', '-created_at')
    readonly_fields     = ('created_at', 'image_preview')  # Keep created_at if it exists

    fieldsets = (
        ('Project Info', {
            'fields': ('title', 'description'),
        }),
        ('Tech Stack', {
            'fields': ('tools',),
            'description': 'Enter tools as a comma-separated list, e.g. "Django, PostgreSQL, Redis".',
        }),
        ('Links', {
            'fields': ('github_link', 'live_link'),
        }),
        ('Media & Order', {
            'fields': ('image', 'image_preview', 'order', 'created_at'),
        }),
    )

    def tools_preview(self, obj):
        tags = obj.tools_list()[:4]
        html = ''.join(
            f'<span style="background:#1a1a1a;color:#FFE600;border:1px solid #333;'
            f'border-radius:4px;padding:1px 8px;margin:2px;font-size:0.7rem;">{t}</span>'
            for t in tags
        )
        if len(obj.tools_list()) > 4:
            html += f'<span style="color:#888;font-size:0.7rem;"> +{len(obj.tools_list()) - 4} more</span>'
        return format_html(html)
    tools_preview.short_description = 'Stack'

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:120px;border-radius:4px;" />', obj.image.url
            )
        return '—'
    image_preview.short_description = 'Preview'


# ─────────────────────────────────────────────
#  EDUCATION
# ─────────────────────────────────────────────

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display       = ('degree', 'school', 'year_range_display', 'order')
    list_display_links = ('degree',)
    list_editable      = ('order',)
    search_fields      = ('school', 'degree', 'program')
    ordering           = ('order', '-year_start')

    def year_range_display(self, obj):
        return obj.year_range()
    year_range_display.short_description = 'Period'


# ─────────────────────────────────────────────
#  SKILL
# ─────────────────────────────────────────────

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display       = ('name', 'category', 'proficiency_bar', 'order')
    list_display_links = ('name',)
    list_editable      = ('order',)
    list_filter        = ('category',)
    search_fields      = ('name',)
    ordering           = ('category', 'order', 'name')

    def proficiency_bar(self, obj):
        pct = obj.proficiency
        color = '#FFE600' if pct >= 70 else ('#00c864' if pct >= 50 else '#ff3c3c')
        return format_html(
            '<div style="width:140px;background:#1a1a1a;border-radius:4px;height:10px;">'
            '<div style="width:{}%;background:{};height:100%;border-radius:4px;"></div>'
            '</div> <small style="color:#888;">{} %</small>',
            pct, color, pct,
        )
    proficiency_bar.short_description = 'Proficiency'

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('name',),
        }),
        ('Contact Info', {
            'fields': ('email', 'location'),
        }),
    )

    list_display = ('name', 'email', 'location', 'updated_at')
    readonly_fields = ('updated_at',)

    def has_add_permission(self, request):
        return not Owner.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False