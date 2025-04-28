from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import Post, Contact


# Post-Modelltests

class PostModelTest(TestCase):
    def test_post_creation(self):
        post = Post.objects.create(title="Testtitel", content="Testinhalt")
        self.assertEqual(post.title, "Testtitel")
        self.assertIsNotNone(post.created_at)

    def test_post_str_method(self):
        post = Post.objects.create(title="Titel", content="...")
        self.assertEqual(str(post), "Titel")


# Contact-Modell + Kontaktformular-Tests

class ContactFormTests(TestCase):
    def test_contact_model_creation(self):
        contact = Contact.objects.create(
            name="Max Mustermann",
            email="max@example.com",
            content="Testnachricht",
            number="1234567890"
        )
        self.assertEqual(contact.name, "Max Mustermann")
        self.assertIn("@", contact.email)

    def test_contact_form_name_too_long(self):
        long_name = 'A' * 31
        response = self.client.post(reverse('contact'), {
            'name': long_name,
            'email': 'test@example.com',
            'content': 'Nachricht',
            'number': '0123456789'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Length of name should be between 2 and 30 characters')
        self.assertEqual(Contact.objects.count(), 0)

    def test_contact_form_success_message_and_redirect(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Sebastien',
            'email': 'seb@example.com',
            'content': 'Das ist eine Testnachricht.',
            'number': '0791234567'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Thank you for contacting me' in str(m) for m in messages))

    def test_contact_form_email_too_long(self):
        long_email = 'a' * 31 + '@test.com'
        response = self.client.post(reverse('contact'), {
            'name': 'Valid Name',
            'email': long_email,
            'content': 'Nachricht',
            'number': '0123456789'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Length of email should be between 2 and 30 characters')
        self.assertEqual(Contact.objects.count(), 0)

    def test_contact_form_number_too_long(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Valid Name',
            'email': 'mail@test.com',
            'content': 'Nachricht',
            'number': '1' * 15  # 15 Zeichen
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Phone number should be between 2 and 14 characters')
        self.assertEqual(Contact.objects.count(), 0)



# Blog-View-Tests

class BlogViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(title="Titel", content="Inhalt")

    def test_post_detail_view(self):
        client = Client()
        url = reverse('post_detail', args=[self.post.id])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_post_list_view(self):
        client = Client()
        url = reverse('blog')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)


# Tests für statische Seiten

class StaticViewTests(TestCase):
    def test_home_view(self):
        response = Client().get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_about_view(self):
        response = Client().get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_skills_view(self):
        response = Client().get(reverse('skills'))
        self.assertEqual(response.status_code, 200)

    def test_projects_view(self):
        response = Client().get(reverse('projects'))
        self.assertEqual(response.status_code, 200)
