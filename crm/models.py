from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator

class Customer(models.Model):
    CUSTOMER_STATUS_CHOICES = [
        ('new', 'New Lead'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal Sent'),
        ('negotiation', 'In Negotiation'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('existing', 'Existing Customer'),
    ]
    
    LEAD_SOURCE_CHOICES = [
        ('website', 'Website'),
        ('referral', 'Referral'),
        ('social_media', 'Social Media'),
        ('phone', 'Phone Call'),
        ('email', 'Email'),
        ('walk_in', 'Walk-in'),
        ('advertisement', 'Advertisement'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    
    # CRM Fields
    status = models.CharField(max_length=20, choices=CUSTOMER_STATUS_CHOICES, default='new')
    lead_source = models.CharField(max_length=20, choices=LEAD_SOURCE_CHOICES, default='website')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_customers')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_contacted = models.DateTimeField(null=True, blank=True)
    
    # Additional Info
    notes = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def total_bookings(self):
        return self.bookings.count()
    
    @property
    def total_revenue(self):
        return sum(booking.total_amount for booking in self.bookings.filter(status='confirmed'))

class EventBooking(models.Model):
    BOOKING_STATUS_CHOICES = [
        ('inquiry', 'Inquiry'),
        ('quoted', 'Quoted'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PACKAGE_CHOICES = [
        ('silver', 'Silver Package - ₹5,000'),
        ('gold', 'Gold Package - ₹6,000'),
        ('diamond', 'Diamond Package - ₹7,000'),
    ]
    
    EVENT_TYPE_CHOICES = [
        ('birthday', 'Birthday Party'),
        ('school', 'School Event'),
        ('corporate', 'Corporate Family Day'),
        ('festival', 'Festival Celebration'),
        ('other', 'Other Kids Event'),
    ]
    
    # Booking Information
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    event_date = models.DateField()
    event_time = models.TimeField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    package = models.CharField(max_length=20, choices=PACKAGE_CHOICES)
    
    # Event Details
    venue_address = models.TextField()
    number_of_children = models.PositiveIntegerField(default=10)
    child_age_group = models.CharField(max_length=50, default="3-12 years")
    special_requests = models.TextField(blank=True, null=True)
    
    # Pricing
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status and Management
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='inquiry')
    assigned_performer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_bookings')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Payment
    advance_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('completed', 'Completed'),
    ], default='pending')
    
    class Meta:
        ordering = ['-event_date']
        
    def __str__(self):
        return f"{self.customer.full_name} - {self.event_type} on {self.event_date}"
    
    def save(self, *args, **kwargs):
        # Calculate total amount
        self.total_amount = self.base_price + self.additional_charges - self.discount
        self.balance_amount = self.total_amount - self.advance_paid
        super().save(*args, **kwargs)

class Interaction(models.Model):
    INTERACTION_TYPE_CHOICES = [
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('whatsapp', 'WhatsApp'),
        ('sms', 'SMS'),
        ('note', 'Note'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    follow_up_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.interaction_type} - {self.customer.full_name} - {self.subject}"

class Task(models.Model):
    TASK_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    booking = models.ForeignKey(EventBooking, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['due_date']
        
    def __str__(self):
        return f"{self.title} - {self.assigned_to.username}"

class Quote(models.Model):
    QUOTE_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='quotes')
    quote_number = models.CharField(max_length=50, unique=True)
    
    # Event Details
    event_type = models.CharField(max_length=20, choices=EventBooking.EVENT_TYPE_CHOICES)
    event_date = models.DateField()
    package = models.CharField(max_length=20, choices=EventBooking.PACKAGE_CHOICES)
    
    # Pricing
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    additional_services = models.TextField(blank=True, null=True)
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status and Validity
    status = models.CharField(max_length=20, choices=QUOTE_STATUS_CHOICES, default='draft')
    valid_until = models.DateField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Notes
    terms_conditions = models.TextField(default="Standard terms and conditions apply.")
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Quote #{self.quote_number} - {self.customer.full_name}"
    
    def save(self, *args, **kwargs):
        if not self.quote_number:
            # Generate quote number
            import datetime
            today = datetime.date.today()
            count = Quote.objects.filter(created_at__date=today).count() + 1
            self.quote_number = f"QT{today.strftime('%Y%m%d')}{count:03d}"
        
        # Calculate total amount
        self.total_amount = self.base_price + self.additional_charges - self.discount
        super().save(*args, **kwargs)