from django.db import models
from django.contrib.auth.models import User


class Tasks(models.Model):
    STATUS_CHOICES = [
        ("assigned", "Assigned"),
        ("in_progress", "In Progress"),
        ("submitted", "Submitted"),
        ("graded", "Graded"),
        ("rejected", "Rejected"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_to = models.ManyToManyField(User,related_name="tasks")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="assigned")
    file = models.FileField(upload_to="submissions/", blank=True, null=True)
    grade = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} → {self.assigned_to} ({self.status})"
