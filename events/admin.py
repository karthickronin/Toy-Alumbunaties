from django.contrib import admin

from .models import EventType, Gallery, Testimonial, Service, ContactInquiry

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_range']
    search_fields = ['name']

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'event_date', 'rating']
    list_filter = ['rating', 'event_date']
    search_fields = ['client_name', 'message']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']
    search_fields = ['title', 'description']

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'event_date', 'event_type', 'created_at']
    list_filter = ['event_type', 'event_date', 'created_at']
    search_fields = ['name', 'email']
    readonly_fields = ['created_at']
