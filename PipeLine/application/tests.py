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
