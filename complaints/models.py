from django.contrib.auth.models import User
from django.db import models


class Complaint(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
    ]

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

    CATEGORY_CHOICES = [
        ("Technical", "Technical"),
        ("Electrical", "Electrical"),
        ("Network", "Network"),
        ("Maintenance", "Maintenance"),
        ("Cleanliness", "Cleanliness"),
        ("Security", "Security"),
        ("Academic", "Academic"),
        ("Administrative", "Administrative"),
        ("Other", "Other"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="complaints",
    )

    title = models.CharField(max_length=255)

    description = models.TextField()

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
    )

    image = models.ImageField(
        upload_to="complaints/",
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.complaint.title}"