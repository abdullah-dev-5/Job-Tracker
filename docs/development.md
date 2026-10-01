# Development

## Prerequisites

- Python 3.13 was used to verify the repository's Django commands.
- PostgreSQL is required by `PipeLine/PipeLine/settings.py`.
- Pillow is required for the optional image upload field and is installed from `requirements.txt`.
- A PostgreSQL database and the credentials listed below must be available before running migrations or the test suite.
- PowerShell is assumed for the Windows activation examples.

## Local setup

Run these commands from the repository root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` with the connection details for the PostgreSQL database. The settings module loads this file from the repository root, one level above the `PipeLine/` Django project directory.

## Environment variables

The settings module reads these variables:

| Variable | Use |
| --- | --- |
| `SECRET_KEY` | Django secret key. The code has a development fallback, but a real local value should be supplied. |
| `DB_NAME` | PostgreSQL database name. |
| `DB_USER` | PostgreSQL user. |
| `DB_PASSWORD` | PostgreSQL password. |
| `DB_HOST` | PostgreSQL host. |
| `DB_PORT` | PostgreSQL port. |

Do not commit `.env`. The checked-in `.env.example` contains placeholders only.

## Running the project

The Django commands must be run from the directory containing `manage.py`:

```powershell
Set-Location .\PipeLine
python manage.py migrate
python manage.py runserver
```

The development server uses Django's default address, `http://127.0.0.1:8000/`. The application dashboard is at `/`, the applications page is at `/applications/`, and the Django admin is at `/admin/`.

## Running tests and checks

From `PipeLine/`, run the system check with:

```powershell
python manage.py check
```

To discover the repository's tests explicitly, run:

```powershell
python manage.py test application.tests
```

The current test module contains eleven tests. Four new tests cover logo lookup success/failure, manual upload replacement, and invalid-upload fallback. Three existing tests fail because the POST view redirects to `/` while those tests expect `/applications/`; this is an existing code/test mismatch, not a setup command to ignore.

## Basic development workflow

1. Activate the virtual environment and ensure `.env` points to a development PostgreSQL database.
2. Make a focused change in the owning Django app or template/static file.
3. Run `python manage.py check`.
4. Run the relevant test module, then the full test suite when the change affects shared views, models, or templates.
5. Create/update migrations when model fields change with `python manage.py makemigrations` and apply them with `python manage.py migrate`.
6. Verify the affected route in the development server and review the rendered behavior on desktop and mobile widths.

## Repository conventions

- Django project code lives under `PipeLine/`; commands are run from that directory.
- The single installed product app is named `application` and uses the `application:` URL namespace.
- Templates extend `base.html`; shared modal markup is included from `templates/components/application_modals.html`.
- Static files are kept under `application/static/` and referenced with Django's `{% static %}` tag.
- Application writes use `ApplicationForm` and Django messages, followed by a redirect.
- Logo lookup is requested through the backend `/api/company-logo/` route; the browser does not contain service credentials.
- Uploaded logos use the optional `logo_image` field and local `MEDIA_ROOT` storage. Automatic logos use the validated `logo_url` field.
- Model status values are defined in `Application.STATUS_CHOICES`; keep form options and UI status filters aligned with them.
- The project uses Django's built-in test runner and `TestCase`/`Client` tests.