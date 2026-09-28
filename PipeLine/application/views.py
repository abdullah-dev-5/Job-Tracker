from django.shortcuts import render


APPLICATIONS = [
    {"id": 1, "company": "Linear", "role": "Senior Product Designer", "status": "Interview", "applied": "Jun 12, 2025", "initials": "LI", "logo_style": "plum"},
    {"id": 2, "company": "Figma", "role": "Product Designer, Growth", "status": "Phone Screen", "applied": "Jun 10, 2025", "initials": "FI", "logo_style": "coral"},
    {"id": 3, "company": "Notion", "role": "Staff Product Designer", "status": "Offer", "applied": "Jun 08, 2025", "initials": "NO", "logo_style": "ink"},
    {"id": 4, "company": "Arc", "role": "Product Designer", "status": "Applied", "applied": "Jun 06, 2025", "initials": "AR", "logo_style": "blue"},
    {"id": 5, "company": "Airbnb", "role": "Experience Designer", "status": "Interview", "applied": "Jun 04, 2025", "initials": "AI", "logo_style": "rejected"},
    {"id": 6, "company": "Dropbox", "role": "Senior UX Designer", "status": "Rejected", "applied": "May 28, 2025", "initials": "DB", "logo_style": "accent"},
    {"id": 7, "company": "Vercel", "role": "Design Systems Lead", "status": "Applied", "applied": "May 25, 2025", "initials": "VE", "logo_style": "ink"},
]

STATUS_COUNTS = [
    {"label": "Applied", "value": 12, "note": "3 this week"},
    {"label": "Phone Screen", "value": 4, "note": "2 upcoming"},
    {"label": "Interview", "value": 3, "note": "1 tomorrow"},
    {"label": "Offer", "value": 2, "note": "Worth celebrating"},
    {"label": "Rejected", "value": 7, "note": "25% of total"},
]

REMINDERS = [
    {"company": "Linear", "task": "Send portfolio follow-up", "due": "Overdue by 1 day", "urgency": "overdue"},
    {"company": "Figma", "task": "Prepare questions for recruiter", "due": "Today, 3:00 PM", "urgency": "today"},
    {"company": "Airbnb", "task": "Confirm interview availability", "due": "Tomorrow", "urgency": "soon"},
    {"company": "Notion", "task": "Review offer details", "due": "Friday, Jun 20", "urgency": "later"},
]


def shared_context():
    return {
        "applications": APPLICATIONS,
        "total_applications_count": len(APPLICATIONS),
        "status_counts": STATUS_COUNTS,
        "status_options": ["All", "Applied", "Phone Screen", "Interview", "Offer", "Rejected"],
        "reminders": REMINDERS,
        "recent_applications": APPLICATIONS[:3],
    }


def dashboard(request):
    """Render the dashboard overview with status counts, reminders, and recent applications."""
    return render(request, "dashboard.html", shared_context())


def applications(request):
    """Render the applications view with filterable list of job applications."""
    return render(request, "applications.html", shared_context())


# Alias home to dashboard for root routing compatibility
home = dashboard