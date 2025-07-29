from django.db import models

class EventType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_range = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Gallery(models.Model):
    title = models.CharField(max_length=200)
    image_url = models.URLField(help_text="URL of the image")
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_image_url = models.URLField(blank=True, help_text="URL of client's image")
    message = models.TextField()
    event_date = models.DateField()
    rating = models.IntegerField(default=5)
    
    def __str__(self):
        return f"{self.client_name} - {self.event_date}"

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=100)  # Font Awesome icon class
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return self.title

class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    event_date = models.DateField()
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.event_date}"
