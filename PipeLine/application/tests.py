from django.test import TestCase, Client
from django.urls import reverse


class ApplicationViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

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
        self.assertContains(response, 'Applications')
        self.assertContains(response, 'Linear')
        self.assertContains(response, 'Senior Product Designer')

    def test_root_url_routes_to_dashboard(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
