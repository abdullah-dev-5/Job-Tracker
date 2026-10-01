import base64
import json
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from application.models import Application, Reminder


class ApplicationViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.app = Application.objects.create(
            company="Linear",
            role="Senior Product Designer",
            status="Applied",
            applied_date="2026-09-01",
            logo_style="accent",
        )

    def test_dashboard_view_resolves_and_renders(self):
        url = reverse('application:dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'components/application_modals.html')
        self.assertIn('status_counts', response.context)
        self.assertIn('reminders', response.context)
        self.assertIn('recent_applications', response.context)
        self.assertIn('applications_json', response.context)
        self.assertContains(response, 'Pipeline')
        self.assertContains(response, 'Follow-up reminders')

    def test_applications_view_resolves_and_renders(self):
        url = reverse('application:applications')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applications.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertIn('applications', response.context)
        self.assertIn('status_options', response.context)
        self.assertIn('applications_json', response.context)
        self.assertContains(response, 'Applications')
        self.assertContains(response, 'Linear')
        self.assertContains(response, 'Senior Product Designer')

    def test_root_url_routes_to_dashboard(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_add_application_modal_post_success(self):
        url = reverse('application:app_modals')
        data = {
            'company': 'Figma',
            'role': 'Product Manager',
            'status': 'Interview',
            'applied_date': '2026-09-15',
            'logo_style': 'coral',
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('application:applications'))

        # Check DB
        figma = Application.objects.get(company='Figma')
        self.assertEqual(figma.role, 'Product Manager')
        self.assertEqual(figma.initials, 'FI')
        self.assertEqual(figma.logo_style, 'coral')
        self.assertEqual(figma.status, 'Interview')

        # Check message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Application added to your pipeline.' in m.message for m in messages))

    def test_edit_application_modal_post_success(self):
        url = reverse('application:app_modals')
        initial_count = Application.objects.count()
        data = {
            'application_id': self.app.id,
            'company': 'Linear App',
            'role': 'Staff Product Designer',
            'status': 'Offer',
            'applied_date': '2026-09-02',
            'logo_style': 'plum',
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('application:applications'))

        # Verify no duplicate created
        self.assertEqual(Application.objects.count(), initial_count)

        self.app.refresh_from_db()
        self.assertEqual(self.app.company, 'Linear App')
        self.assertEqual(self.app.role, 'Staff Product Designer')
        self.assertEqual(self.app.initials, 'LI')
        self.assertEqual(self.app.logo_style, 'plum')
        self.assertEqual(self.app.status, 'Offer')

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Application updated.' in m.message for m in messages))

    def test_application_modal_get_redirects(self):
        url = reverse('application:app_modals')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('application:applications'))

    def test_application_modal_invalid_form(self):
        url = reverse('application:app_modals')
        data = {
            'company': '',  # company is required
            'role': '',
            'status': 'Applied',
            'applied_date': '',
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('application:applications'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Could not save the application' in m.message for m in messages))

    @patch('application.views.urlopen')
    def test_company_logo_lookup_returns_logo_url(self, mock_urlopen):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps([{'domain': 'microsoft.com'}]).encode()

        mock_urlopen.return_value = Response()
        response = self.client.get(reverse('application:company_logo'), {'company': 'Microsoft'})
        self.assertEqual(response.json()['logo_url'], 'https://www.google.com/s2/favicons?domain=microsoft.com&sz=128')

    @patch('application.views.urlopen', side_effect=TimeoutError)
    def test_company_logo_lookup_failure_is_empty(self, mock_urlopen):
        response = self.client.get(reverse('application:company_logo'), {'company': 'Unknown Company'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['logo_url'], '')

    def test_application_accepts_manual_logo_and_replaces_it(self):
        logo_bytes = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=')
        first_logo = SimpleUploadedFile('first.png', logo_bytes, content_type='image/png')
        response = self.client.post(reverse('application:app_modals'), {
            'company': 'Figma',
            'role': 'Product Manager',
            'status': 'Applied',
            'applied_date': '2026-09-15',
            'logo_url': 'https://logo.clearbit.com/figma.com',
            'logo_image': first_logo,
        })
        self.assertEqual(response.status_code, 302)
        application = Application.objects.get(company='Figma')
        self.assertTrue(application.logo_image.name.startswith('company_logos/'))
        self.assertEqual(application.logo_url, '')

        second_logo = SimpleUploadedFile('second.png', logo_bytes, content_type='image/png')
        self.client.post(reverse('application:app_modals'), {
            'application_id': application.id,
            'company': 'Figma',
            'role': 'Product Manager',
            'status': 'Offer',
            'applied_date': '2026-09-15',
            'logo_url': '',
            'logo_image': second_logo,
        })
        application.refresh_from_db()
        self.assertTrue(application.logo_image.name.startswith('company_logos/'))
        self.assertEqual(application.status, 'Offer')

    def test_invalid_logo_does_not_block_application_creation(self):
        invalid_logo = SimpleUploadedFile('logo.txt', b'not-an-image', content_type='text/plain')
        response = self.client.post(reverse('application:app_modals'), {
            'company': 'Unknown Company',
            'role': 'Designer',
            'status': 'Applied',
            'applied_date': '2026-09-15',
            'logo_url': '',
            'logo_image': invalid_logo,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Application.objects.filter(company='Unknown Company').exists())
