from django import forms
from django.contrib.auth.models import User
from .models import Customer, EventBooking, Interaction, Task, Quote

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'company',
            'address', 'city', 'state', 'pincode',
            'status', 'lead_source', 'notes'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 9876543210'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name (Optional)'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PIN Code'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'lead_source': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Additional notes about the customer...'}),
        }

class EventBookingForm(forms.ModelForm):
    class Meta:
        model = EventBooking
        fields = [
            'customer', 'event_date', 'event_time', 'event_type', 'package',
            'venue_address', 'number_of_children', 'child_age_group',
            'special_requests', 'base_price', 'additional_charges', 'discount',
            'advance_paid', 'status'
        ]
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'package': forms.Select(attrs={'class': 'form-select'}),
            'venue_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Complete venue address'}),
            'number_of_children': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': '10'}),
            'child_age_group': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '3-12 years'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special requests or requirements...'}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '5000.00'}),
            'additional_charges': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'advance_paid': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default prices based on package
        self.fields['base_price'].help_text = "Silver: ₹5,000 | Gold: ₹6,000 | Diamond: ₹7,000"

class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['interaction_type', 'subject', 'description', 'follow_up_date']
        widgets = {
            'interaction_type': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Interaction subject'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed description of the interaction...'}),
            'follow_up_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'customer', 'booking', 'assigned_to', 'priority', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Task description...'}),
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'booking': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True)
        self.fields['customer'].required = False
        self.fields['booking'].required = False

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = [
            'customer', 'event_type', 'event_date', 'package',
            'base_price', 'additional_services', 'additional_charges',
            'discount', 'valid_until', 'terms_conditions', 'notes'
        ]
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'package': forms.Select(attrs={'class': 'form-select'}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'additional_services': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional services included...'}),
            'additional_charges': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'valid_until': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'terms_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Internal notes...'}),
        }

class CustomerSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search customers...',
            'autocomplete': 'off'
        })
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Customer.CUSTOMER_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    lead_source = forms.ChoiceField(
        choices=[('', 'All Sources')] + Customer.LEAD_SOURCE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class BookingSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search bookings...',
            'autocomplete': 'off'
        })
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + EventBooking.BOOKING_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )