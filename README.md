# Pipeline

Pipeline is a Django-based **job application manager** designed to help organize and manage the job application process.

The project is currently under active development, with the core structure and interface in place while the final feature set is still being defined.

## Tech Stack

* **Backend:** Django
* **Frontend:** HTML, CSS, JavaScript
* **Database:** Django-supported database configuration
* **Configuration:** Environment variables using `.env`

## Project Structure

```text
Job Application Tracker/
│
├── PipeLine/
│   ├── application/
│   │   ├── migrations/
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   └── style.css
│   │   │   └── js/
│   │   │       └── app.js
│   │   ├── templates/
│   │   │   ├── components/
│   │   │   │   └── application_modals.html
│   │   │   ├── applications.html
│   │   │   ├── base.html
│   │   │   └── dashboard.html
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── PipeLine/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   └── manage.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── Project_MVP.txt
```

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd "Job Application Tracker"
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create your `.env` file from `.env.example`:

```powershell
copy .env.example .env
```

Open `.env` and update the required values for your local environment.

> **Important:** Never commit your real `.env` file to Git. Keep secrets and credentials inside environment variables.

### 5. Run migrations

From the directory containing `manage.py`:

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

The application should then be available at:

```text
http://127.0.0.1:8000/
```

## Current Status

Pipeline is currently an **early-stage MVP / work in progress**.

The Django project structure, templates, styling, JavaScript, dashboard, and application-management interface are being developed. The final set of features is not yet finalized.

Future development will focus on defining and implementing the core job-application management workflow.

## Planned Development

Potential areas for future development include:

* Job application tracking
* Application status management
* Dashboard improvements
* Application details
* Notes and additional information
* Search and filtering
* Improved application workflow
* Additional productivity features

These features are subject to change as the project develops.

## Development

Pipeline is being developed as a Django web application with a straightforward architecture intended to remain easy to maintain and extend.

The frontend currently uses standard:

* HTML
* CSS
* JavaScript

rather than a separate frontend framework.

## Contributing

The project is currently under active development. Contributions, suggestions, and ideas are welcome as the application's direction and feature set continue to evolve.

## License

License information has not yet been specified.
