from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def dashboard_login(request):
    """Dashboard login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'dashboard/login.html')

def dashboard_logout(request):
    """Dashboard logout view"""
    logout(request)
    return redirect('dashboard:login')

@login_required
def dashboard_home(request):
    """Dashboard home page"""
    return render(request, 'dashboard/home.html')

@login_required
def content_management(request):
    """Content management interface"""
    return render(request, 'dashboard/content.html')

@login_required
def portfolio_management(request):
    """Portfolio management interface"""
    return render(request, 'dashboard/portfolio.html')

@login_required
def inquiry_management(request):
    """Contact inquiry management"""
    return render(request, 'dashboard/inquiries.html')

@login_required
def team_management(request):
    """Team member management"""
    return render(request, 'dashboard/team.html')
