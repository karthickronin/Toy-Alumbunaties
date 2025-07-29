from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import Http404
from .simple_models import SAMPLE_CUSTOMERS, STATUS_CHOICES, LEAD_SOURCE_CHOICES

def crm_login(request):
    """CRM Login View"""
    if request.user.is_authenticated:
        return redirect('crm:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                next_url = request.GET.get('next', 'crm:dashboard')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'crm/vyzor_login.html', {'form': form})

def crm_logout(request):
    """CRM Logout View"""
    user_name = request.user.first_name or request.user.username if request.user.is_authenticated else "User"
    logout(request)
    messages.success(request, f'Goodbye {user_name}! You have been logged out successfully.')
    return redirect('crm:login')

@login_required
def dashboard(request):
    """Main CRM Dashboard with sample data"""
    # Sample metrics
    total_customers = len(SAMPLE_CUSTOMERS)
    new_leads = len([c for c in SAMPLE_CUSTOMERS if c.status == 'new'])
    active_bookings = 3  # Sample data
    monthly_revenue = 25000  # Sample data
    
    # Recent customers (first 5)
    recent_customers = SAMPLE_CUSTOMERS[:5]
    
    # Sample upcoming events
    upcoming_events = [
        {'customer': {'full_name': 'Suresh Muthukutty'}, 'event_type': 'birthday', 'package': 'diamond', 'event_date': '2025-07-25', 'total_amount': 7000},
        {'customer': {'full_name': 'Priya Sharma'}, 'event_type': 'birthday', 'package': 'gold', 'event_date': '2025-07-28', 'total_amount': 6000},
    ]
    
    # Sample pending tasks
    pending_tasks = [
        {'title': 'Follow up with Priya Sharma', 'customer': {'full_name': 'Priya Sharma'}, 'priority': 'high', 'due_date': '2025-07-23'},
        {'title': 'Prepare quote for Meera Patel', 'customer': {'full_name': 'Meera Patel'}, 'priority': 'medium', 'due_date': '2025-07-24'},
    ]
    
    # Sample lead sources data
    lead_sources = [
        {'lead_source': 'website', 'count': 3},
        {'lead_source': 'referral', 'count': 1},
        {'lead_source': 'social_media', 'count': 1},
    ]
    
    # Sample booking status data
    booking_status = [
        {'status': 'inquiry', 'count': 2},
        {'status': 'confirmed', 'count': 1},
        {'status': 'completed', 'count': 2},
    ]
    
    context = {
        'total_customers': total_customers,
        'new_leads': new_leads,
        'active_bookings': active_bookings,
        'completed_bookings': 2,
        'monthly_revenue': monthly_revenue,
        'pending_revenue': 13000,
        'recent_customers': recent_customers,
        'upcoming_events': upcoming_events,
        'pending_tasks': pending_tasks,
        'lead_sources': lead_sources,
        'booking_status': booking_status,
    }
    
    return render(request, 'crm/vyzor_dashboard.html', context)

@login_required
def customer_list(request):
    """Customer list with sample data"""
    customers = SAMPLE_CUSTOMERS.copy()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        customers = [c for c in customers if 
                    search_query.lower() in c.first_name.lower() or 
                    search_query.lower() in c.last_name.lower() or 
                    search_query.lower() in c.email.lower() or 
                    search_query.lower() in c.phone.lower()]
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        customers = [c for c in customers if c.status == status_filter]
    
    # Filter by lead source
    source_filter = request.GET.get('source', '')
    if source_filter:
        customers = [c for c in customers if c.lead_source == source_filter]
    
    # Create a simple paginator-like object
    class SimplePaginator:
        def __init__(self, items):
            self.count = len(items)
    
    class SimpleCustomerList:
        def __init__(self, items):
            self.object_list = items
            self.paginator = SimplePaginator(items)
        
        def __iter__(self):
            return iter(self.object_list)
        
        def __len__(self):
            return len(self.object_list)
        
        def __getitem__(self, index):
            return self.object_list[index]
    
    customers_obj = SimpleCustomerList(customers)
    
    context = {
        'customers': customers_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'source_filter': source_filter,
        'status_choices': STATUS_CHOICES,
        'source_choices': LEAD_SOURCE_CHOICES,
    }
    
    return render(request, 'crm/vyzor_customer_list.html', context)

@login_required
def customer_detail(request, customer_id):
    """Customer detail view with sample data"""
    try:
        customer = next(c for c in SAMPLE_CUSTOMERS if c.id == int(customer_id))
    except (StopIteration, ValueError):
        raise Http404("Customer not found")
    
    # Sample related data
    bookings = []
    interactions = []
    tasks = []
    quotes = []
    
    if customer.id == 4:  # Suresh Muthukutty - has bookings
        bookings = [
            {
                'id': 1,
                'event_date': '2025-07-25',
                'event_type': 'birthday',
                'package': 'diamond',
                'total_amount': 7000,
                'status': 'confirmed',
                'get_event_type_display': lambda: 'Birthday Party',
                'get_package_display': lambda: 'Diamond Package - ₹7,000',
                'get_status_display': lambda: 'Confirmed'
            }
        ]
        interactions = [
            {
                'interaction_type': 'call',
                'subject': 'Initial inquiry about birthday party',
                'description': 'Customer called asking about entertainment packages for 5-year-old birthday party. Interested in character appearances and games.',
                'created_by': {'first_name': 'Admin', 'last_name': 'User'},
                'created_at': '2025-07-20 10:30:00',
                'get_interaction_type_display': lambda: 'Phone Call'
            }
        ]
    
    context = {
        'customer': customer,
        'bookings': bookings,
        'interactions': interactions,
        'tasks': tasks,
        'quotes': quotes,
    }
    
    return render(request, 'crm/vyzor_customer_detail.html', context)

@login_required
def customer_create(request):
    """Create new customer - placeholder"""
    if request.method == 'POST':
        messages.success(request, 'Customer creation will be implemented when database is ready!')
        return redirect('crm:customer_list')
    
    return render(request, 'crm/customer_form.html', {'title': 'Add New Customer'})

@login_required
def customer_edit(request, customer_id):
    """Edit customer - placeholder"""
    try:
        customer = next(c for c in SAMPLE_CUSTOMERS if c.id == int(customer_id))
    except (StopIteration, ValueError):
        raise Http404("Customer not found")
    
    if request.method == 'POST':
        messages.success(request, f'Customer {customer.full_name} editing will be implemented when database is ready!')
        return redirect('crm:customer_detail', customer_id=customer.id)
    
    return render(request, 'crm/customer_form.html', {
        'customer': customer, 
        'title': f'Edit {customer.full_name}'
    })

@login_required
def booking_list(request):
    """Booking list - placeholder"""
    # Sample bookings
    bookings = [
        {
            'id': 1,
            'customer': {'full_name': 'Suresh Muthukutty'},
            'event_date': '2025-07-25',
            'event_type': 'birthday',
            'package': 'diamond',
            'total_amount': 7000,
            'status': 'confirmed',
            'assigned_performer': {'first_name': 'Deepak', 'last_name': 'Performer'}
        }
    ]
    
    class SimpleBookingList:
        def __init__(self, items):
            self.object_list = items
            self.paginator = type('obj', (object,), {'count': len(items)})()
        
        def __iter__(self):
            return iter(self.object_list)
        
        def __len__(self):
            return len(self.object_list)
        
        def __getitem__(self, index):
            return self.object_list[index]
    
    context = {
        'bookings': SimpleBookingList(bookings),
        'status_choices': [('inquiry', 'Inquiry'), ('confirmed', 'Confirmed'), ('completed', 'Completed')],
        'search_query': '',
        'status_filter': '',
        'date_from': '',
        'date_to': '',
    }
    
    return render(request, 'crm/vyzor_booking_list.html', context)

@login_required
def booking_create(request, customer_id=None):
    """Create booking - placeholder"""
    customer = None
    if customer_id:
        try:
            customer = next(c for c in SAMPLE_CUSTOMERS if c.id == int(customer_id))
        except (StopIteration, ValueError):
            pass
    
    if request.method == 'POST':
        messages.success(request, 'Booking creation will be implemented when database is ready!')
        return redirect('crm:booking_list')
    
    return render(request, 'crm/booking_form.html', {
        'customer': customer,
        'title': 'Create New Booking'
    })

@login_required
def booking_detail(request, booking_id):
    """Booking detail - placeholder"""
    booking = {
        'id': booking_id,
        'customer': {'full_name': 'Suresh Muthukutty'},
        'event_date': '2025-07-25',
        'event_type': 'birthday',
        'package': 'diamond',
        'total_amount': 7000,
        'status': 'confirmed'
    }
    
    context = {
        'booking': booking,
        'tasks': [],
    }
    
    return render(request, 'crm/booking_detail.html', context)

@login_required
def task_list(request):
    """Task list - placeholder"""
    tasks = [
        {
            'title': 'Follow up with Priya Sharma',
            'customer': {'full_name': 'Priya Sharma'},
            'assigned_to': {'first_name': 'Admin', 'last_name': 'User'},
            'status': 'pending',
            'priority': 'high',
            'due_date': '2025-07-23',
            'created_by': {'first_name': 'Admin', 'last_name': 'User'}
        }
    ]
    
    class SimpleTaskList:
        def __init__(self, items):
            self.object_list = items
            self.paginator = type('obj', (object,), {'count': len(items)})()
        
        def __iter__(self):
            return iter(self.object_list)
        
        def __len__(self):
            return len(self.object_list)
        
        def __getitem__(self, index):
            return self.object_list[index]
    
    context = {
        'tasks': SimpleTaskList(tasks),
        'status_choices': [('pending', 'Pending'), ('completed', 'Completed')],
        'priority_choices': [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        'status_filter': '',
        'priority_filter': '',
    }
    
    return render(request, 'crm/vyzor_task_list.html', context)

@login_required
def add_interaction(request, customer_id):
    """Add interaction - placeholder"""
    try:
        customer = next(c for c in SAMPLE_CUSTOMERS if c.id == int(customer_id))
    except (StopIteration, ValueError):
        raise Http404("Customer not found")
    
    if request.method == 'POST':
        messages.success(request, 'Interaction will be saved when database is ready!')
        return redirect('crm:customer_detail', customer_id=customer.id)
    
    return render(request, 'crm/interaction_form.html', {
        'customer': customer,
        'title': f'Add Interaction - {customer.full_name}'
    })

@login_required
def reports(request):
    """Reports - placeholder"""
    context = {
        'customer_growth': [{'month': '2025-07', 'count': 5}],
        'revenue_by_package': [
            {'package': 'diamond', 'total_revenue': 7000, 'booking_count': 1},
            {'package': 'gold', 'total_revenue': 6000, 'booking_count': 1},
        ],
        'lead_performance': [
            {'lead_source': 'website', 'customer_count': 3, 'conversion_rate': 33.3},
            {'lead_source': 'referral', 'customer_count': 1, 'conversion_rate': 100.0},
        ],
        'booking_trends': [{'month': '2025-07', 'booking_count': 2, 'total_revenue': 13000}],
        'start_date': '2025-04-22',
        'end_date': '2025-07-22',
    }
    
    return render(request, 'crm/reports.html', context)