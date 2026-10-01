import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
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
            "logoUrl": app.logo_url,
            "logoImage": app.logo_image.url if app.logo_image else "",
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


home = dashboard


def applications(request):
    """Render the applications page."""
    return render(request, "applications.html", shared_context())


def applications_modal(request):
    """Create a new application, update one, or delete one if action=delete is posted."""
    if request.method != "POST":
        return redirect("application:applications")

    application_id = request.POST.get("application_id")
    action = request.POST.get("action")

    # ── Delete ───────────────────────────────────────────────────────
    if action == "delete" and application_id:
        application = get_object_or_404(Application, pk=application_id)
        application.delete()
        messages.success(request, "Application deleted.")
        return redirect("application:applications")

    # ── Create / Update (unchanged) ─────────────────────────────────
    instance = get_object_or_404(Application, pk=application_id) if application_id else None

    form = ApplicationForm(request.POST, request.FILES, instance=instance)
    if form.is_valid():
        application = form.save(commit=False)
        if form.cleaned_data.get("logo_image"):
            application.logo_url = ""
        application.save()
        messages.success(
            request,
            "Application updated." if instance else "Application added to your pipeline.",
        )
    elif set(form.errors) == {"logo_image"}:
        # A bad optional upload must not block the application itself.
        fallback_form = ApplicationForm(request.POST, instance=instance)
        if fallback_form.is_valid():
            fallback_form.save()
            messages.warning(request, "The application was saved, but the logo upload was not used.")
        else:
            messages.error(request, "Could not save the application. Please check the form.")
    else:
        messages.error(request, "Could not save the application. Please check the form.")

    return redirect("application:applications")


def company_logo(request):
    """Resolve a company name to a Clearbit logo URL without exposing credentials."""
    company = request.GET.get("company", "").strip()
    if not company:
        return JsonResponse({"logo_url": "", "domain": ""})

    endpoint = "https://autocomplete.clearbit.com/v1/companies/suggest?query=" + quote(company)
    try:
        request = Request(endpoint, headers={"Accept": "application/json", "User-Agent": "Pipeline/1.0"})
        with urlopen(request, timeout=5) as response:
            suggestions = json.load(response)
    except (OSError, URLError, TimeoutError, ValueError, json.JSONDecodeError):
        return JsonResponse({"logo_url": "", "domain": ""})

    if not isinstance(suggestions, list):
        return JsonResponse({"logo_url": "", "domain": ""})

    company_key = " ".join(company.casefold().split())
    matches = [
        item for item in suggestions
        if isinstance(item, dict) and isinstance(item.get("domain"), str) and item.get("domain", "").strip()
    ]
    exact_match = next(
        (item for item in matches if " ".join(str(item.get("name", "")).casefold().split()) == company_key),
        None,
    )
    selected = exact_match or (matches[0] if matches else None)
    domain = selected.get("domain", "").strip().lower() if selected else ""
    if not domain or "/" in domain or " " in domain:
        return JsonResponse({"logo_url": "", "domain": ""})

    return JsonResponse({
        "logo_url": "https://www.google.com/s2/favicons?domain=" + quote(domain, safe=".") + "&sz=128",
        "domain": domain,
    })
