from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from .models import Customer, EventBooking, Interaction, Task, Quote
# from .forms import CustomerForm, EventBookingForm, InteractionForm, TaskForm, QuoteForm

@login_required
def dashboard(request):
    """Main CRM Dashboard"""
    # Get date range for filtering (last 30 days by default)
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Key metrics
    total_customers = Customer.objects.count()
    new_leads = Customer.objects.filter(status='new').count()
    active_bookings = EventBooking.objects.filter(status__in=['inquiry', 'quoted', 'confirmed']).count()
    completed_bookings = EventBooking.objects.filter(status='completed', event_date__range=[start_date, end_date]).count()
    
    # Revenue metrics
    monthly_revenue = EventBooking.objects.filter(
        status='completed',
        event_date__range=[start_date, end_date]
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    pending_revenue = EventBooking.objects.filter(
        status__in=['confirmed', 'quoted']
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Recent activities
    recent_customers = Customer.objects.order_by('-created_at')[:5]
    
    # Get upcoming events with proper error handling
    try:
        upcoming_events = EventBooking.objects.select_related('customer').filter(
            event_date__gte=timezone.now().date(),
            status='confirmed'
        ).order_by('event_date')[:5]
    except:
        upcoming_events = []
    
    # Get pending tasks with proper error handling
    try:
        pending_tasks = Task.objects.select_related('customer', 'assigned_to').filter(
            assigned_to=request.user,
            status__in=['pending', 'in_progress']
        ).order_by('due_date')[:5]
    except:
        pending_tasks = []
    
    # Lead source analysis
    lead_sources = Customer.objects.values('lead_source').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Booking status distribution
    booking_status = EventBooking.objects.values('status').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'total_customers': total_customers,
        'new_leads': new_leads,
        'active_bookings': active_bookings,
        'completed_bookings': completed_bookings,
        'monthly_revenue': monthly_revenue,
        'pending_revenue': pending_revenue,
        'recent_customers': recent_customers,
        'upcoming_events': upcoming_events,
        'pending_tasks': pending_tasks,
        'lead_sources': lead_sources,
        'booking_status': booking_status,
    }
    
    return render(request, 'crm/dashboard.html', context)

@login_required
def customer_list(request):
    """Customer list with filtering and search"""
    customers = Customer.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        customers = customers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(company__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        customers = customers.filter(status=status_filter)
    
    # Filter by lead source
    source_filter = request.GET.get('source')
    if source_filter:
        customers = customers.filter(lead_source=source_filter)
    
    # Pagination
    paginator = Paginator(customers, 20)
    page_number = request.GET.get('page')
    customers = paginator.get_page(page_number)
    
    context = {
        'customers': customers,
        'search_query': search_query,
        'status_filter': status_filter,
        'source_filter': source_filter,
        'status_choices': Customer.CUSTOMER_STATUS_CHOICES,
        'source_choices': Customer.LEAD_SOURCE_CHOICES,
    }
    
    return render(request, 'crm/customer_list.html', context)

@login_required
def customer_detail(request, customer_id):
    """Customer detail view with all related information"""
    customer = get_object_or_404(Customer, id=customer_id)
    
    # Get related data
    bookings = customer.bookings.all().order_by('-event_date')
    interactions = customer.interactions.all().order_by('-created_at')
    tasks = customer.tasks.all().order_by('-due_date')
    quotes = customer.quotes.all().order_by('-created_at')
    
    context = {
        'customer': customer,
        'bookings': bookings,
        'interactions': interactions,
        'tasks': tasks,
        'quotes': quotes,
    }
    
    return render(request, 'crm/customer_detail.html', context)

@login_required
def customer_create(request):
    """Create new customer"""
    if request.method == 'POST':
        # Simple form processing without Django forms for now
        customer = Customer.objects.create(
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            company=request.POST.get('company', ''),
            address=request.POST.get('address', ''),
            city=request.POST.get('city', ''),
            state=request.POST.get('state', ''),
            pincode=request.POST.get('pincode', ''),
            status=request.POST.get('status', 'new'),
            lead_source=request.POST.get('lead_source', 'website'),
            notes=request.POST.get('notes', ''),
            assigned_to=request.user
        )
        messages.success(request, f'Customer {customer.full_name} created successfully!')
        return redirect('crm:customer_detail', customer_id=customer.id)
    
    return render(request, 'crm/customer_form.html', {'title': 'Add New Customer'})

@login_required
def customer_edit(request, customer_id):
    """Edit existing customer"""
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        # Simple form processing without Django forms for now
        customer.first_name = request.POST.get('first_name', customer.first_name)
        customer.last_name = request.POST.get('last_name', customer.last_name)
        customer.email = request.POST.get('email', customer.email)
        customer.phone = request.POST.get('phone', customer.phone)
        customer.save()
        messages.success(request, f'Customer {customer.full_name} updated successfully!')
        return redirect('crm:customer_detail', customer_id=customer.id)
    
    return render(request, 'crm/customer_form.html', {
        'customer': customer, 
        'title': f'Edit {customer.full_name}'
    })

@login_required
def booking_list(request):
    """Event bookings list"""
    bookings = EventBooking.objects.select_related('customer', 'assigned_performer').all()
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        bookings = bookings.filter(event_date__gte=date_from)
    if date_to:
        bookings = bookings.filter(event_date__lte=date_to)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        bookings = bookings.filter(
            Q(customer__first_name__icontains=search_query) |
            Q(customer__last_name__icontains=search_query) |
            Q(customer__email__icontains=search_query) |
            Q(venue_address__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(bookings, 20)
    page_number = request.GET.get('page')
    bookings = paginator.get_page(page_number)
    
    context = {
        'bookings': bookings,
        'status_choices': EventBooking.BOOKING_STATUS_CHOICES,
        'search_query': search_query,
        'status_filter': status_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    
    return render(request, 'crm/booking_list.html', context)

@login_required
def booking_create(request, customer_id=None):
    """Create new booking"""
    customer = None
    if customer_id:
        customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        # Simple booking creation for now
        messages.success(request, 'Booking functionality will be implemented!')
        return redirect('crm:booking_list')
    
    return render(request, 'crm/booking_form.html', {
        'customer': customer,
        'title': 'Create New Booking'
    })

@login_required
def booking_detail(request, booking_id):
    """Booking detail view"""
    booking = get_object_or_404(EventBooking, id=booking_id)
    tasks = booking.tasks.all().order_by('-due_date')
    
    context = {
        'booking': booking,
        'tasks': tasks,
    }
    
    return render(request, 'crm/booking_detail.html', context)

@login_required
def task_list(request):
    """Task management"""
    tasks = Task.objects.select_related('customer', 'assigned_to', 'created_by').all()
    
    # Filter by assigned user
    if not request.user.is_superuser:
        tasks = tasks.filter(assigned_to=request.user)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    
    # Filter by priority
    priority_filter = request.GET.get('priority')
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    
    # Pagination
    paginator = Paginator(tasks, 20)
    page_number = request.GET.get('page')
    tasks = paginator.get_page(page_number)
    
    context = {
        'tasks': tasks,
        'status_choices': Task.TASK_STATUS_CHOICES,
        'priority_choices': Task.PRIORITY_CHOICES,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
    }
    
    return render(request, 'crm/task_list.html', context)

@login_required
def add_interaction(request, customer_id):
    """Add interaction to customer"""
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        # Simple interaction creation for now
        interaction = Interaction.objects.create(
            customer=customer,
            interaction_type=request.POST.get('interaction_type', 'note'),
            subject=request.POST.get('subject', ''),
            description=request.POST.get('description', ''),
            created_by=request.user
        )
        
        # Update customer's last contacted date
        customer.last_contacted = timezone.now()
        customer.save()
        
        messages.success(request, 'Interaction added successfully!')
        return redirect('crm:customer_detail', customer_id=customer.id)
    
    return render(request, 'crm/interaction_form.html', {
        'customer': customer,
        'title': f'Add Interaction - {customer.full_name}'
    })

@login_required
def reports(request):
    """CRM Reports and Analytics"""
    # Date range for reports
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=90)  # Last 3 months
    
    # Customer acquisition over time
    customer_growth = Customer.objects.filter(
        created_at__date__range=[start_date, end_date]
    ).extra(
        select={'month': 'strftime("%%Y-%%m", created_at)'}
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    # Revenue by package
    revenue_by_package = EventBooking.objects.filter(
        status='completed',
        event_date__range=[start_date, end_date]
    ).values('package').annotate(
        total_revenue=Sum('total_amount'),
        booking_count=Count('id')
    ).order_by('-total_revenue')
    
    # Top performing lead sources
    lead_performance = Customer.objects.values('lead_source').annotate(
        customer_count=Count('id'),
        conversion_rate=Count('bookings') * 100.0 / Count('id')
    ).order_by('-customer_count')
    
    # Monthly booking trends
    booking_trends = EventBooking.objects.filter(
        event_date__range=[start_date, end_date]
    ).extra(
        select={'month': 'strftime("%%Y-%%m", event_date)'}
    ).values('month').annotate(
        booking_count=Count('id'),
        total_revenue=Sum('total_amount')
    ).order_by('month')
    
    context = {
        'customer_growth': customer_growth,
        'revenue_by_package': revenue_by_package,
        'lead_performance': lead_performance,
        'booking_trends': booking_trends,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'crm/reports.html', context)

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
    
    return render(request, 'crm/login.html', {'form': form})

def crm_logout(request):
    """CRM Logout View"""
    user_name = request.user.first_name or request.user.username
    logout(request)
    messages.success(request, f'Goodbye {user_name}! You have been logged out successfully.')
    return redirect('crm:login')