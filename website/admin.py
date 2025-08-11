from django.contrib import admin
from .models import Service, Portfolio, PortfolioImage, ContactInquiry, TeamMember, SiteContent

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured', 'order', 'created_at']
    list_filter = ['featured', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['featured', 'order']

class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 1

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'category', 'featured', 'order', 'created_at']
    list_filter = ['category', 'featured', 'created_at']
    search_fields = ['title', 'client', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['featured', 'order']
    filter_horizontal = ['services']
    inlines = [PortfolioImageInline]

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'company']
    readonly_fields = ['created_at']
    list_editable = ['status']

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'active', 'order']
    list_filter = ['active']
    search_fields = ['name', 'position']
    list_editable = ['active', 'order']

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ['key', 'title', 'updated_at']
    search_fields = ['key', 'title', 'content']
