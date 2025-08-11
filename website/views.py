from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
import json
from .models import Service, Portfolio, TeamMember, ContactInquiry, SiteContent

def home(request):
    """Homepage view matching Fantasy.co aesthetic"""
    featured_services = Service.objects.filter(featured=True)[:3]
    # Only get portfolio items that have images
    featured_portfolio = Portfolio.objects.filter(featured=True).exclude(featured_image='')[:4]
    
    context = {
        'featured_services': featured_services,
        'featured_portfolio': featured_portfolio,
    }
    return render(request, 'website/home.html', context)

def homepage(request):
    """Redirect old homepage to new home view"""
    return home(request)

def services(request):
    """Services overview page"""
    all_services = Service.objects.all()
    context = {
        'services': all_services,
    }
    return render(request, 'website/services.html', context)

def service_detail(request, slug):
    """Individual service detail page"""
    service = get_object_or_404(Service, slug=slug)
    related_portfolio = Portfolio.objects.filter(services=service)[:3]
    
    context = {
        'service': service,
        'related_portfolio': related_portfolio,
    }
    return render(request, 'website/service_detail.html', context)

def portfolio(request):
    """Portfolio gallery page"""
    category = request.GET.get('category')
    if category:
        projects = Portfolio.objects.filter(category=category).exclude(featured_image='')
    else:
        projects = Portfolio.objects.all().exclude(featured_image='')
    
    categories = Portfolio.CATEGORY_CHOICES
    
    context = {
        'projects': projects,
        'categories': categories,
        'current_category': category,
    }
    return render(request, 'website/portfolio.html', context)

def portfolio_detail(request, slug):
    """Individual portfolio project detail page"""
    project = get_object_or_404(Portfolio, slug=slug)
    related_projects = Portfolio.objects.filter(category=project.category).exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'website/portfolio_detail.html', context)

def about(request):
    """About page"""
    team_members = TeamMember.objects.filter(active=True)
    
    # Get dynamic content
    try:
        mission_content = SiteContent.objects.get(key='about_mission').content
    except SiteContent.DoesNotExist:
        mission_content = "At Admire, we are Brand for Brands. We believe in the power of exceptional design and innovative technology to transform businesses and create meaningful connections."
    
    context = {
        'team_members': team_members,
        'mission_content': mission_content,
    }
    return render(request, 'website/about.html', context)

def contact(request):
    """Contact page"""
    return render(request, 'website/contact.html')

@csrf_exempt
@require_http_methods(["POST"])
def contact_submit(request):
    """Handle contact form submission without Django forms"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()
        company = data.get('company', '').strip()
        
        if not all([name, email, message]):
            return JsonResponse({
                'success': False,
                'error': 'Please fill in all required fields.'
            }, status=400)
        
        # Save to database
        inquiry = ContactInquiry.objects.create(
            name=name,
            email=email,
            company=company,
            message=message
        )
        
        # Send email notification
        try:
            email_subject = f"New Contact Inquiry from {name}"
            email_message = f"""
New contact inquiry received:

Name: {name}
Email: {email}
Company: {company}
Message: {message}

Submitted at: {inquiry.created_at}
            """
            
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                ['founder.admire@gmail.com'],
                fail_silently=False,
            )
        except Exception as e:
            # Log email error but don't fail the request
            print(f"Email sending failed: {e}")
        
        return JsonResponse({
            'success': True,
            'message': 'Thank you for your message. We\'ll get back to you soon!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid data format.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Something went wrong. Please try again.'
        }, status=500)
