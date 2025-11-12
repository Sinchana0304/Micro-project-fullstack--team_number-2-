from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# ----------------------------
# Custom User Model
# ----------------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ('organiser', 'Organiser'),
        ('donor', 'Donor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

# ----------------------------
# Disaster Model
# ----------------------------
class Disaster(models.Model):
    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    organiser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    urgency_level = models.CharField(max_length=20, choices=URGENCY_CHOICES)
    image = models.ImageField(upload_to='disaster_images/', blank=True, null=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    # ✅ Bank details for manual donation
    bank_account_name = models.CharField(max_length=100)
    bank_account_number = models.CharField(max_length=30)
    ifsc_code = models.CharField(max_length=15)
    upi_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.title} ({self.urgency_level})"

# ----------------------------
# Donation Model
# ----------------------------
class Donation(models.Model):
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    disaster = models.ForeignKey(Disaster, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # ✅ Manual payment details
    transaction_id = models.CharField(max_length=100)
    proof_image = models.ImageField(upload_to='donation_proofs/', blank=True, null=True)

    message = models.TextField(blank=True)
    donated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.username} → {self.disaster.title} (₹{self.amount})"

# ----------------------------
# Message Model
# ----------------------------
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    disaster = models.ForeignKey(Disaster, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} → {self.recipient.username} ({self.disaster.title})"

# ----------------------------
# Feedback Model
# ----------------------------
class Feedback(models.Model):
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organiser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_feedback')
    disaster = models.ForeignKey(Disaster, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.username} → {self.organiser.username} ({self.rating}★)"
