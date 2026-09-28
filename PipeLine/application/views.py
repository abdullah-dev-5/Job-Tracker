from django.shortcuts import render
from .models import Reminder, Application


def shared_context():
    applications = Application.objects.all()

    status_counts = []

    for value, label in Application.STATUS_CHOICES:
        status_counts.append({
            "label": label,
            "value": applications.filter(status=value).count(),
        })

    return {
        "applications": applications,
        "total_applications_count": applications.count(),
        "status_counts": status_counts,
        "status_options": ["All"] + [
            label for _, label in Application.STATUS_CHOICES
        ],
        "reminders": Reminder.objects.all(),
        "recent_applications": applications[:3],
    }


def dashboard(request):
    """Render the dashboard overview with status counts, reminders, and recent applications."""
    return render(request, "dashboard.html", shared_context())


def applications(request):
    """Render the applications view with filterable list of job applications."""
    return render(request, "applications.html", shared_context())


home = dashboard