from django.db import models

class Patient(models.Model):
    # Choices for enum fields
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    STAGE_CHOICES = [
        ('Stage 0', 'Stage 0'),
        ('Stage I', 'Stage I'),
        ('Stage II', 'Stage II'),
        ('Stage III', 'Stage III'),
        ('Stage IV', 'Stage IV'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Under Treatment', 'Under Treatment'),
        ('Recovered', 'Recovered'),
        ('Critical', 'Critical'),
    ]

    # Required Fields
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    # Optional Fields
    contact = models.CharField(max_length=20, blank=True, help_text="Patient's phone number")
    email = models.EmailField(max_length=254, blank=True)
    diagnosis = models.CharField(max_length=255, blank=True)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)
    medical_history = models.TextField(blank=True)

    # Auto-generated Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} (ID: {self.pk})'

