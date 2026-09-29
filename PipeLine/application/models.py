from django.db import models


class Application(models.Model):
    STATUS_CHOICES = [
        ("Applied", "Applied"),
        ("Phone Screen", "Phone Screen"),
        ("Interview", "Interview"),
        ("Offer", "Offer"),
        ("Rejected", "Rejected"),
    ]

    company = models.CharField(max_length=100)
    role = models.CharField(max_length=150)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Applied")
    applied_date = models.DateField()
    initials = models.CharField(max_length=2, blank=True)
    logo_style = models.CharField(max_length=30, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-applied_date"]

    def save(self, *args, **kwargs):
        self.initials = self.company.strip()[:2].upper()
        if not self.logo_style:
            self.logo_style = "accent"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.company} - {self.role}"


class Reminder(models.Model):
    class Urgency(models.TextChoices):
        OVERDUE = "overdue", "Overdue"
        TODAY = "today", "Today"
        SOON = "soon", "Soon"
        LATER = "later", "Later"

    application = models.ForeignKey( Application, on_delete=models.CASCADE, related_name="reminders")
    task = models.CharField(max_length=200)
    due_date = models.DateTimeField()
    urgency = models.CharField(max_length=20, choices=Urgency.choices, default=Urgency.LATER)
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["due_date"]

    def __str__(self):
        return f"{self.application.company} - {self.task}"