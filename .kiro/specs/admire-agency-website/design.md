# Design Document

## Overview

The Admire agency website will be a sophisticated, modern web application built with Django that showcases the company's advertising and IT capabilities. The design follows contemporary agency website patterns with a focus on visual storytelling, professional presentation, and seamless user experience. The architecture separates public-facing content from administrative functionality through distinct Django applications.

## Architecture

### High-Level Architecture

```mermaid
graph TB
    A[Client Browser] --> B[Django Web Server]
    B --> C[Main Website App]
    B --> D[Dashboard App]
    B --> E[Static Files/Media]
    C --> F[PostgreSQL Database]
    D --> F
    G[Email Service] --> H[founder.admire@gmail.com]
    C --> G
```

### Application Structure

The project will consist of two main Django applications:

1. **Main Website App (`website`)**: Handles all public-facing functionality
2. **Dashboard App (`dashboard`)**: Provides administrative interface for content management

### Technology Stack

- **Backend**: Django 4.2+ with Python 3.11+
- **Frontend**: Bootstrap 5.3+ with custom CSS/JavaScript
- **Database**: PostgreSQL (production) / SQLite (development)
- **Static Files**: Django's static file handling with potential CDN integration
- **Email**: Django's email backend configured for Gmail SMTP

## Components and Interfaces

### Main Website App Components

#### 1. Homepage Component
- **Hero Section**: Dynamic banner with Admire branding and "Brand for Brands" slogan
- **Services Preview**: Animated cards showcasing key service areas
- **Portfolio Highlights**: Featured project carousel
- **Contact CTA**: Prominent contact section with social links

#### 2. Services Component
- **Service Categories**: Advertising and IT services with detailed descriptions
- **Service Detail Pages**: Individual pages for each service offering
- **Case Study Integration**: Embedded portfolio examples relevant to each service

#### 3. Portfolio Component
- **Gallery View**: Masonry-style layout for project thumbnails
- **Project Detail View**: Full case study pages with images, descriptions, and outcomes
- **Filtering System**: Category-based filtering (advertising, IT, branding, web development)

#### 4. About Component
- **Company Story**: Mission, vision, and "Brand for Brands" philosophy
- **Team Profiles**: Key team member information and photos
- **Company Culture**: Visual storytelling elements

#### 5. Contact Component
- **Contact Form**: Custom-built form (no Django forms) with validation
- **Contact Information**: Email (founder.admire@gmail.com) and social media (@admire.brand)
- **Form Processing**: Backend handling with email notifications

### Dashboard App Components

#### 1. Authentication System
- **Login Interface**: Secure login for authorized users
- **Session Management**: Django's built-in session handling
- **Permission Controls**: Role-based access to different dashboard sections

#### 2. Content Management
- **Homepage Editor**: Interface to update hero content, service previews
- **Service Manager**: Add/edit service descriptions and details
- **Portfolio Manager**: Upload and manage project images, descriptions, case studies
- **About Page Editor**: Update company information and team profiles

#### 3. Inquiry Management
- **Contact Form Submissions**: View and manage incoming inquiries
- **Email Integration**: Direct email responses from dashboard
- **Status Tracking**: Mark inquiries as read, responded, or closed

## Data Models

### Core Models

```python
# Website Models
class Service:
    title = CharField(max_length=200)
    slug = SlugField(unique=True)
    description = TextField()
    icon = ImageField()
    featured = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

class Portfolio:
    title = CharField(max_length=200)
    slug = SlugField(unique=True)
    client = CharField(max_length=200, blank=True)
    category = CharField(max_length=100)
    description = TextField()
    featured_image = ImageField()
    gallery_images = ManyToManyField('PortfolioImage')
    services = ManyToManyField(Service)
    featured = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)

class PortfolioImage:
    portfolio = ForeignKey(Portfolio)
    image = ImageField()
    caption = CharField(max_length=500, blank=True)
    order = PositiveIntegerField(default=0)

class ContactInquiry:
    name = CharField(max_length=200)
    email = EmailField()
    company = CharField(max_length=200, blank=True)
    message = TextField()
    status = CharField(max_length=50, default='new')
    created_at = DateTimeField(auto_now_add=True)
    responded_at = DateTimeField(null=True, blank=True)

class TeamMember:
    name = CharField(max_length=200)
    position = CharField(max_length=200)
    bio = TextField()
    photo = ImageField()
    order = PositiveIntegerField(default=0)
    active = BooleanField(default=True)

class SiteContent:
    key = CharField(max_length=100, unique=True)
    title = CharField(max_length=500, blank=True)
    content = TextField()
    updated_at = DateTimeField(auto_now=True)
```

### URL Structure

```
# Main Website URLs
/ - Homepage
/services/ - Services overview
/services/<slug>/ - Individual service pages
/portfolio/ - Portfolio gallery
/portfolio/<slug>/ - Individual project pages
/about/ - About page
/contact/ - Contact page

# Dashboard URLs
/dashboard/ - Dashboard home
/dashboard/login/ - Authentication
/dashboard/content/ - Content management
/dashboard/portfolio/ - Portfolio management
/dashboard/inquiries/ - Contact inquiries
/dashboard/team/ - Team management
```

## Error Handling

### Frontend Error Handling
- **Form Validation**: Client-side validation with Bootstrap styling
- **AJAX Error Handling**: Graceful handling of form submission errors
- **404/500 Pages**: Custom error pages matching site design
- **Loading States**: Visual feedback during form submissions and page loads

### Backend Error Handling
- **Model Validation**: Django model-level validation for data integrity
- **View Error Handling**: Try-catch blocks for database operations
- **Email Failures**: Fallback handling if email sending fails
- **File Upload Errors**: Validation and error messages for image uploads

### Security Considerations
- **CSRF Protection**: Django's built-in CSRF protection for all forms
- **Input Sanitization**: Proper escaping of user-generated content
- **File Upload Security**: Validation of uploaded file types and sizes
- **Dashboard Authentication**: Secure login with session management

## Testing Strategy

### Unit Testing
- **Model Tests**: Validation of all model methods and properties
- **View Tests**: Testing of all view functions and class-based views
- **Form Processing Tests**: Custom form validation and processing logic
- **Utility Function Tests**: Helper functions and custom template tags

### Integration Testing
- **End-to-End Workflows**: Complete user journeys from homepage to contact
- **Dashboard Functionality**: Content management workflows
- **Email Integration**: Contact form to email delivery testing
- **File Upload Workflows**: Portfolio image upload and display

### Frontend Testing
- **Responsive Design Testing**: Cross-device and cross-browser compatibility
- **JavaScript Functionality**: Form validation and interactive elements
- **Performance Testing**: Page load times and image optimization
- **Accessibility Testing**: WCAG compliance for inclusive design

### Deployment Testing
- **Static File Serving**: Proper CSS, JS, and image delivery
- **Database Migrations**: Safe deployment of schema changes
- **Environment Configuration**: Production vs development settings
- **SSL/Security Headers**: HTTPS and security header implementation

## Design System

### Visual Design Principles
- **Modern Minimalism**: Clean, uncluttered layouts with strategic white space
- **Bold Typography**: Strong headings with readable body text
- **Professional Color Palette**: Sophisticated colors that convey trust and creativity
- **High-Quality Imagery**: Professional photography and graphics throughout

### Bootstrap Customization
- **Custom CSS Variables**: Override Bootstrap defaults for brand consistency
- **Component Extensions**: Custom components built on Bootstrap foundation
- **Responsive Breakpoints**: Optimized for mobile-first design approach
- **Animation and Transitions**: Subtle animations for enhanced user experience

### Content Strategy
- **Brand Voice**: Professional yet approachable tone reflecting "Brand for Brands"
- **Visual Hierarchy**: Clear information architecture guiding user attention
- **Call-to-Action Placement**: Strategic positioning of contact and inquiry prompts
- **SEO Optimization**: Content structured for search engine visibility