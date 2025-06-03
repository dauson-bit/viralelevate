from django.db import models

class PaymentSupportRequest(models.Model):
    ISSUE_CHOICES = [
        ('Payment not going through', 'Payment not going through'),
        ('Double charged', 'Double charged'),
        ('Need to change payment method', 'Need to change payment method'),
        ('Other issue', 'Other issue'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    issue = models.CharField(max_length=100, choices=ISSUE_CHOICES)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.issue}'

class Package(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
class Service(models.Model):
    packages = models.ForeignKey(Package, related_name='services', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField(default="This is a description")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    unit = models.CharField(max_length=50, help_text="e.g., followers, likes, views" ,blank=True)

    def __str__(self):
        return f"{self.name} ({self.packages.name})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    link = models.URLField(help_text="Link to the content that needs boosting")
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.service.name} ({self.customer_name})"
