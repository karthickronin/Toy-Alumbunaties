from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Customer, EventBooking, Interaction, Task, Quote

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'status', 'lead_source', 'assigned_to', 'total_bookings', 'created_at']
    list_filter = ['status', 'lead_source', 'assigned_to', 'created_at', 'city']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'company']
    list_editable = ['status', 'assigned_to']
    readonly_fields = ['created_at', 'updated_at', 'total_bookings', 'total_revenue']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'company')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'pincode'),
            'classes': ('collapse',)
        }),
        ('CRM Information', {
            'fields': ('status', 'lead_source', 'assigned_to', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_contacted'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('total_bookings', 'total_revenue'),
            'classes': ('collapse',)
        }),
    )
    
    def total_bookings(self, obj):
        return obj.total_bookings
    total_bookings.short_description = 'Total Bookings'
    
    def total_revenue(self, obj):
        return f"₹{obj.total_revenue:,.2f}"
    total_revenue.short_description = 'Total Revenue'

@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'event_type', 'event_date', 'package', 'status', 'total_amount', 'payment_status', 'assigned_performer']
    list_filter = ['status', 'event_type', 'package', 'payment_status', 'event_date', 'assigned_performer']
    search_fields = ['customer__first_name', 'customer__last_name', 'customer__email', 'venue_address']
    list_editable = ['status', 'assigned_performer']
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer',)
        }),
        ('Event Details', {
            'fields': ('event_type', 'event_date', 'event_time', 'package', 'venue_address', 'number_of_children', 'child_age_group', 'special_requests')
        }),
        ('Pricing', {
            'fields': ('base_price', 'additional_charges', 'discount', 'total_amount')
        }),
        ('Payment', {
            'fields': ('advance_paid', 'balance_amount', 'payment_status')
        }),
        ('Management', {
            'fields': ('status', 'assigned_performer')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['total_amount', 'balance_amount', 'created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer', 'assigned_performer')

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ['customer', 'interaction_type', 'subject', 'created_by', 'created_at', 'follow_up_date']
    list_filter = ['interaction_type', 'created_by', 'created_at', 'follow_up_date']
    search_fields = ['customer__first_name', 'customer__last_name', 'subject', 'description']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Interaction Details', {
            'fields': ('customer', 'interaction_type', 'subject', 'description')
        }),
        ('Follow-up', {
            'fields': ('follow_up_date',)
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_by', 'created_at']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by for new objects
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer', 'assigned_to', 'status', 'priority', 'due_date', 'created_by']
    list_filter = ['status', 'priority', 'assigned_to', 'due_date', 'created_by']
    search_fields = ['title', 'description', 'customer__first_name', 'customer__last_name']
    list_editable = ['status', 'priority']
    date_hierarchy = 'due_date'
    
    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description', 'customer', 'booking')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'status', 'priority', 'due_date')
        }),
        ('Timestamps', {
            'fields': ('created_by', 'created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_by', 'created_at', 'updated_at', 'completed_at']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by for new objects
            obj.created_by = request.user
        if obj.status == 'completed' and not obj.completed_at:
            obj.completed_at = timezone.now()
        super().save_model(request, obj, form, change)

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['quote_number', 'customer', 'event_type', 'event_date', 'total_amount', 'status', 'valid_until', 'created_at']
    list_filter = ['status', 'event_type', 'package', 'created_at', 'valid_until']
    search_fields = ['quote_number', 'customer__first_name', 'customer__last_name', 'customer__email']
    readonly_fields = ['quote_number', 'total_amount', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Quote Information', {
            'fields': ('quote_number', 'customer', 'status')
        }),
        ('Event Details', {
            'fields': ('event_type', 'event_date', 'package')
        }),
        ('Pricing', {
            'fields': ('base_price', 'additional_services', 'additional_charges', 'discount', 'total_amount')
        }),
        ('Validity', {
            'fields': ('valid_until', 'sent_at')
        }),
        ('Additional Information', {
            'fields': ('terms_conditions', 'notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer')

# Custom admin site configuration
admin.site.site_header = "Toy Alumbunaties CRM"
admin.site.site_title = "CRM Admin"
admin.site.index_title = "Customer Relationship Management"