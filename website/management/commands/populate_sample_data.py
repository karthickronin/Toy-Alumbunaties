from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from website.models import Service, Portfolio, TeamMember, SiteContent
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create Services
        services_data = [
            {
                'title': 'Brand Identity',
                'slug': 'brand-identity',
                'description': 'We create distinctive visual identities that capture the essence of your brand and resonate with your target audience. From logo design to comprehensive brand guidelines, we ensure consistency across all touchpoints.',
                'short_description': 'Creating distinctive visual identities that capture the essence of your brand.',
                'featured': True,
                'order': 1
            },
            {
                'title': 'Web Development',
                'slug': 'web-development',
                'description': 'Building modern, responsive websites and applications that deliver exceptional user experiences. We focus on performance, accessibility, and scalability to ensure your digital presence stands out.',
                'short_description': 'Building modern, responsive websites and applications.',
                'featured': True,
                'order': 2
            },
            {
                'title': 'Digital Marketing',
                'slug': 'digital-marketing',
                'description': 'Strategic digital campaigns that drive engagement, build communities, and deliver measurable results. We combine creativity with data-driven insights to maximize your marketing ROI.',
                'short_description': 'Strategic digital campaigns that drive engagement and results.',
                'featured': True,
                'order': 3
            },
            {
                'title': 'IT Solutions',
                'slug': 'it-solutions',
                'description': 'Comprehensive technology solutions that streamline operations and drive innovation. From system integration to custom software development, we help businesses leverage technology effectively.',
                'short_description': 'Comprehensive technology solutions for modern businesses.',
                'featured': False,
                'order': 4
            }
        ]
        
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                slug=service_data['slug'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f'Created service: {service.title}')
        
        # Create Portfolio items
        portfolio_data = [
            {
                'title': 'TechStart Brand Identity',
                'slug': 'techstart-brand-identity',
                'client': 'TechStart Inc.',
                'category': 'branding',
                'description': 'Complete brand identity redesign for a growing tech startup. We created a modern, scalable visual system that reflects their innovative approach and appeals to their target market.',
                'short_description': 'Complete brand identity redesign for a growing tech startup.',
                'featured': True,
                'order': 1
            },
            {
                'title': 'E-commerce Platform',
                'slug': 'ecommerce-platform',
                'client': 'RetailPro',
                'category': 'web',
                'description': 'Custom e-commerce platform built with modern technologies. Features include inventory management, payment processing, and advanced analytics dashboard.',
                'short_description': 'Custom e-commerce platform with advanced features.',
                'featured': True,
                'order': 2
            },
            {
                'title': 'Digital Campaign Launch',
                'slug': 'digital-campaign-launch',
                'client': 'Fashion Forward',
                'category': 'advertising',
                'description': 'Multi-channel digital marketing campaign that increased brand awareness by 300% and drove significant sales growth across all platforms.',
                'short_description': 'Multi-channel digital marketing campaign.',
                'featured': True,
                'order': 3
            },
            {
                'title': 'Custom CRM System',
                'slug': 'custom-crm-system',
                'client': 'BusinessPro',
                'category': 'it',
                'description': 'Tailored customer relationship management system that streamlined operations and improved customer satisfaction scores by 40%.',
                'short_description': 'Tailored CRM system for improved operations.',
                'featured': True,
                'order': 4
            }
        ]
        
        for portfolio_data in portfolio_data:
            portfolio, created = Portfolio.objects.get_or_create(
                slug=portfolio_data['slug'],
                defaults=portfolio_data
            )
            if created:
                self.stdout.write(f'Created portfolio item: {portfolio.title}')
        
        # Create Team Members
        team_data = [
            {
                'name': 'Alex Johnson',
                'position': 'Creative Director',
                'bio': 'With over 10 years of experience in brand design and creative strategy, Alex leads our creative vision and ensures every project exceeds expectations.',
                'active': True,
                'order': 1
            },
            {
                'name': 'Sarah Chen',
                'position': 'Lead Developer',
                'bio': 'Sarah brings technical expertise and innovative solutions to every project. She specializes in modern web technologies and scalable architecture.',
                'active': True,
                'order': 2
            }
        ]
        
        for team_data in team_data:
            team_member, created = TeamMember.objects.get_or_create(
                name=team_data['name'],
                defaults=team_data
            )
            if created:
                self.stdout.write(f'Created team member: {team_member.name}')
        
        # Create Site Content
        content_data = [
            {
                'key': 'about_mission',
                'title': 'About Mission',
                'content': 'At Admire, we are Brand for Brands. We believe in the power of exceptional design and innovative technology to transform businesses and create meaningful connections. Our mission is to help brands discover their authentic voice and amplify it through strategic creative solutions that drive real results.'
            }
        ]
        
        for content_data in content_data:
            content, created = SiteContent.objects.get_or_create(
                key=content_data['key'],
                defaults=content_data
            )
            if created:
                self.stdout.write(f'Created site content: {content.key}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))