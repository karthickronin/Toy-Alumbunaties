from django.shortcuts import render, redirect
from django.contrib import messages

def home(request):
    # Toy Alumbunaties sample data
    featured_gallery = [
        {'title': 'Teddy Character Performance', 'media_url': '/static/teddy.mp4', 'category': 'characters', 'type': 'video'},
        {'title': 'Birthday Party Fun', 'media_url': '/static/gallery/IMG_2369.jpg', 'category': 'parties', 'type': 'image'},
        {'title': 'Happy Kids Moments', 'media_url': '/static/gallery/IMG_2138.jpg', 'category': 'photos', 'type': 'image'},
    ]
    
    testimonials = [
        {'client_name': 'Suresh Muthukutty', 'message': 'Toy Alumbunaties made my daughter\'s birthday absolutely magical! The teddy bear character was amazing and the kids loved every moment.', 'rating': 5},
        {'client_name': 'Yugabharathi', 'message': 'Professional service and such entertaining performances! The football freestyle show was incredible. Highly recommend for any kids event.', 'rating': 5},
        {'client_name': 'Gold Sharon', 'message': 'The interactive games and photo sessions were perfect! Our little ones had the best time ever. Thank you Toy Alumbunaties!', 'rating': 5},
    ]
    
    services = [
        {'title': 'Character Appearances', 'description': 'Meet & Greet sessions with adorable teddy bear costumes that bring joy and excitement to your events.', 'icon': 'fas fa-mask'},
        {'title': 'Dance Performances', 'description': 'Lively and fun dance moves that get everyone moving and create unforgettable entertainment moments.', 'icon': 'fas fa-music'},
        {'title': 'Interactive Games', 'description': 'Engaging activities and fun games specially designed to keep kids entertained and active throughout the event.', 'icon': 'fas fa-gamepad'},
    ]
    
    context = {
        'featured_gallery': featured_gallery,
        'testimonials': testimonials,
        'services': services,
    }
    return render(request, 'events/home.html', context)

def services(request):
    services = [
        {
            'title': 'Silver Package',
            'description': 'Perfect for small gatherings and intimate celebrations with essential entertainment',
            'icon': 'fas fa-medal',
            'price': '₹5,000',
            'package_type': 'silver',
            'duration': '2 Hours',
            'features': [
                'Character Appearances (Teddy Costume)',
                'Basic Dance Performances',
                'Interactive Games (2-3 activities)',
                'Photo Session with Character',
                'Basic Welcome Greeting'
            ]
        },
        {
            'title': 'Gold Package',
            'description': 'Most popular choice with comprehensive entertainment for memorable celebrations',
            'icon': 'fas fa-crown',
            'price': '₹6,000',
            'package_type': 'gold',
            'duration': '3 Hours',
            'popular': True,
            'features': [
                'Character Appearances (Multiple Costumes)',
                'Full Dance Performances',
                'Interactive Games & Activities (4-5 games)',
                'Football Freestyle Show',
                'Professional Photo & Video Session',
                'Humble Welcome & Guest Interaction',
                'Fun Activities with Kids'
            ]
        },
        {
            'title': 'Diamond Package',
            'description': 'Premium all-inclusive package for the ultimate celebration experience',
            'icon': 'fas fa-gem',
            'price': '₹7,000',
            'package_type': 'diamond',
            'duration': '4 Hours',
            'features': [
                'Premium Character Appearances (All Costumes)',
                'Complete Dance & Entertainment Shows',
                'Full Interactive Entertainment Suite',
                'Professional Football Freestyle',
                'Extended Photo & Video Sessions',
                'VIP Welcome & Guest Services',
                'Complete Games & Activities Package',
                'Special Surprise Elements',
                'Event Coordination Support'
            ]
        }
    ]
    context = {'services': services}
    return render(request, 'events/services.html', context)

from django.shortcuts import render

def gallery(request):
    # Real videos and images from your static folder
    gallery_items = [
        # Videos from static/videos/
        
        {
            'title': 'Birthday Party Entertainment 1',
            'category': 'parties',
            'type': 'video',
            'media_url': '/static/videos/toy_alumbunaties-20250717-0002.mp4',
            'description': 'Fun-filled birthday party celebration'
        },
        {
            'title': 'Interactive Games Session',
            'category': 'games',
            'type': 'video',
            'media_url': '/static/videos/toy_alumbunaties-20250717-0003.mp4',
            'description': 'Engaging games and activities with children'
        },
        {
            'title': 'Character Meet & Greet',
            'category': 'characters',
            'type': 'video',
            'media_url': '/static/videos/toy_alumbunaties-20250717-0004.mp4',
            'description': 'Kids meeting and playing with characters'
        },
        {
            'title': 'Birthday Celebration Fun',
            'category': 'parties',
            'type': 'video',
            'media_url': '/static/videos/toy_alumbunaties-20250717-0005.mp4',
            'description': 'Memorable birthday party moments'
        },
        {
            'title': 'Fun Activities & Games',
            'category': 'games',
            'type': 'video',
            'media_url': '/static/videos/toy_alumbunaties-20250717-0006.mp4',
            'description': 'Interactive play and entertainment'
        },
        {
            'title': 'Dance & Entertainment Show',
            'category': 'dance',
            'type': 'video',
            'media_url': '/static/videos/toy_alumbunaties-20250717-0008.mp4',
            'description': 'Lively dance performance for kids'
        },
        {
            'title': 'Kids Party Entertainment',
            'category': 'parties',
            'type': 'video',
            'media_url': '/static/videos/toy_alumbunaties-20250717-0010.mp4',
            'description': 'Complete party entertainment package'
        },
        
        # Images from static/gallery/
        {
            'title': 'Happy Kids Moments',
            'category': 'photos',
            'type': 'image',
            'media_url': '/static/gallery/IMG_2138.jpg',
            'description': 'Joyful moments captured during events'
        },
        {
            'title': 'Event Highlights',
            'category': 'photos',
            'type': 'image',
            'media_url': '/static/gallery/IMG_2369.jpg',
            'description': 'Best moments from our performances'
        },
        {
            'title': 'Party Celebration',
            'category': 'photos',
            'type': 'image',
            'media_url': '/static/gallery/IMG_2495.JPG',
            'description': 'Beautiful party celebration moments'
        },
        {
            'title': 'Teddy Character Performance',
            'category': 'characters',
            'type': 'video',
            'media_url': '/static/teddy.mp4',
            'description': 'Amazing teddy bear character entertaining kids'
        },
        {
            'title': 'Fun Dance Performance',
            'category': 'dance',
            'type': 'video',
            'media_url': '/static/videos/Selfie pulla 😍…#post #reelsviral #coimbatoremapla #toyalumbanaties #fun #girlspower #tamil #tre.mp4',
            'description': 'Energetic dance show with kids participation'
        },
    ]
    
    # Get unique categories for filter buttons
    categories = list(set([item['category'] for item in gallery_items]))
    
    context = {
        'gallery_items': gallery_items,
        'categories': categories,
    }
    return render(request, 'events/gallery.html', context)


def about(request):
    testimonials = [
        {'client_name': 'Priya Sharma', 'message': 'Toy Alumbunaties made my daughter\'s birthday absolutely magical! The teddy bear character was amazing and the kids loved every moment.', 'rating': 5},
        {'client_name': 'Rajesh Kumar', 'message': 'Professional service and such entertaining performances! The football freestyle show was incredible. Highly recommend for any kids event.', 'rating': 5},
        {'client_name': 'Meera Patel', 'message': 'The interactive games and photo sessions were perfect! Our little ones had the best time ever. Thank you Toy Alumbunaties!', 'rating': 5},
    ]
    context = {'testimonials': testimonials}
    return render(request, 'events/about.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        event_date = request.POST.get('event_date')
        event_type = request.POST.get('event_type')
        message = request.POST.get('message')
        
        # For now, just show a success message
        messages.success(request, 'Thank you! Your inquiry has been sent successfully. We will contact you within 24 hours to discuss your fun event!')
        return redirect('contact')
    
    event_types = [
        {'id': 1, 'name': 'Birthday Party'},
        {'id': 2, 'name': 'School Event'},
        {'id': 3, 'name': 'Corporate Family Day'},
        {'id': 4, 'name': 'Festival Celebration'},
        {'id': 5, 'name': 'Other Kids Event'},
    ]
    context = {'event_types': event_types}
    return render(request, 'events/contact.html')