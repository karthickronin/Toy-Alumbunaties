# Simple CRM data structures that don't require database migrations
# This is a temporary solution until Django installation issues are resolved

class SimpleCustomer:
    """Simple customer data structure"""
    def __init__(self, id, first_name, last_name, email, phone, status='new', lead_source='website', notes=''):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.status = status
        self.lead_source = lead_source
        self.notes = notes
        self.created_at = None
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def total_bookings(self):
        return 0  # Placeholder
    
    @property
    def total_revenue(self):
        return 0  # Placeholder

# Sample data for demonstration
SAMPLE_CUSTOMERS = [
    SimpleCustomer(1, "Priya", "Sharma", "priya.sharma@email.com", "+91 9876543210", "new", "website", "Interested in birthday party package"),
    SimpleCustomer(2, "Rajesh", "Kumar", "rajesh.kumar@email.com", "+91 9876543211", "contacted", "referral", "Looking for school event entertainment"),
    SimpleCustomer(3, "Meera", "Patel", "meera.patel@email.com", "+91 9876543212", "qualified", "social_media", "Corporate family day event"),
    SimpleCustomer(4, "Suresh", "Muthukutty", "suresh.m@email.com", "+91 9876543213", "won", "phone", "Booked Diamond package for birthday"),
    SimpleCustomer(5, "Yugabharathi", "R", "yugabharathi@email.com", "+91 9876543214", "new", "website", "Inquiry about football freestyle show"),
]

STATUS_CHOICES = [
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