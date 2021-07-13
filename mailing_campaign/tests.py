from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from rest_framework import response


class ContactListAPITest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user('aliteralshoe', password='lace')
        user.save()
        user = User.objects.create_user('aliteralshirt', password='button')

    def test_post_contact_list(self):
        client = Client()
        with open('mailing_campaign/examples/test.json') as contact_list:
            contact_list_json = contact_list.read()
            # Test unauthorized access
            response = client.post('/mailing_campaign/', contact_list_json, content_type='application/json')
            self.assertEqual(response.status_code, 401)
            # Test authorized access posting json
            client.login(username='aliteralshoe', password='lace')
            response = client.post('/mailing_campaign/', contact_list_json, content_type='application/json')
            self.assertEqual(response.status_code, 201)
            client.logout()

        # Test invalid json    
        with open('mailing_campaign/examples/mail_test.json') as contact_list:
            client.login(username='aliteralshoe', password='lace')
            response = client.post('/mailing_campaign/', contact_list.read(), content_type='application/json')
            self.assertEqual(response.status_code, 400)
    

    def test_get_contact_list(self):
        client = Client()
        response = client.get('/mailing_campaign/')
        self.assertEqual(response.status_code, 401)
        client.login(username='aliteralshoe', password='lace')
        response = client.get('/mailing_campaign/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"contact_lists":[]}')
        with open('mailing_campaign/examples/test.json') as contact_list:
            contact_list_json = contact_list.read()
            client.post('/mailing_campaign/', contact_list_json, content_type='application/json')
            client.post('/mailing_campaign/', contact_list_json, content_type='application/json')
        response = client.get('/mailing_campaign/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"contact_lists":[{"id":1,"contacts":[{"first_name":"For","last_name":"Ever","email_address":"for@ever.de"},{"first_name":"Never","last_name":"Again","email_address":"never@again.com"}]},{"id":2,"contacts":[{"first_name":"For","last_name":"Ever","email_address":"for@ever.de"},{"first_name":"Never","last_name":"Again","email_address":"never@again.com"}]}]}')
        client.logout()
        client.login(username='aliteralshirt', password='button')
        response = client.get('/mailing_campaign/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"contact_lists":[]}')
        