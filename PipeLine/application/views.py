from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ApplicationForm
from .models import Application, Reminder


def shared_context():
    applications = Application.objects.all()

    status_counts = []
    for value, label in Application.STATUS_CHOICES:
        status_counts.append({
            "label": label,
            "value": applications.filter(status=value).count(),
        })

    # Data for the JavaScript "view / edit" modals
    applications_json = [
        {
            "id": app.id,
            "company": app.company,
            "role": app.role,
            "status": app.status,
            "applied": app.applied_date.strftime("%b %d, %Y"),
            "applied_iso": app.applied_date.isoformat(),
            "initials": app.initials,
            "logoStyle": app.logo_style,
        }
        for app in applications
    ]

    return {
        "applications": applications,
        "applications_json": applications_json,
        "total_applications_count": applications.count(),
        "status_counts": status_counts,
        "status_options": ["All"] + [label for _, label in Application.STATUS_CHOICES],
        "reminders": Reminder.objects.select_related("application"),
        "recent_applications": applications.order_by("-updated_at")[:3],
    }


def dashboard(request):
    """Render the dashboard overview."""
    return render(request, "dashboard.html", shared_context())


def applications(request):
    """Render the applications page."""
    return render(request, "applications.html", shared_context())


def applications_modal(request):
    """Create a new application, or update one if application_id is posted."""
    if request.method != "POST":
        return redirect("application:applications")

    application_id = request.POST.get("application_id")
    instance = get_object_or_404(Application, pk=application_id) if application_id else None

    form = ApplicationForm(request.POST, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(
            request,
            "Application updated." if instance else "Application added to your pipeline.",
        )
    else:
        messages.error(request, "Could not save the application. Please check the form.")

    return redirect("application:dashboard")


home = dashboard
