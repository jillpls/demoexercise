from rest_framework.renderers import JSONRenderer
from mailing_campaign.mail import Campaign, CampaignPost, generate_instances
from mailing_campaign.serializers import CampaignPostSerializer, CampaignSerializer
from mailing_campaign.models import ContactList, Video
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from rest_framework import response, serializers


class ContactListAPITest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user('aliteralshoe', password='lace')
        user.save()
        user = User.objects.create_user('aliteralshirt', password='button')
        user.save()

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
        
        # Test unauthorized access
        response = client.get('/mailing_campaign/')
        self.assertEqual(response.status_code, 401)
        
        # Test authorized access with empty lists
        client.login(username='aliteralshoe', password='lace')
        response = client.get('/mailing_campaign/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'"{\\"contact_lists\\":[]}"')
        
        # Test authorized access with existing lists 
        with open('mailing_campaign/examples/test.json') as contact_list:
            contact_list_json = contact_list.read()
            client.post('/mailing_campaign/', contact_list_json, content_type='application/json')
            client.post('/mailing_campaign/', contact_list_json, content_type='application/json')
        response = client.get('/mailing_campaign/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'"{\\"contact_lists\\":[{\\"id\\":1,\\"contacts\\":[{\\"first_name\\":\\"For\\",\\"last_name\\":\\"Ever\\",\\"email_address\\":\\"for@ever.de\\"},{\\"first_name\\":\\"Never\\",\\"last_name\\":\\"Again\\",\\"email_address\\":\\"never@again.com\\"}]},{\\"id\\":2,\\"contacts\\":[{\\"first_name\\":\\"For\\",\\"last_name\\":\\"Ever\\",\\"email_address\\":\\"for@ever.de\\"},{\\"first_name\\":\\"Never\\",\\"last_name\\":\\"Again\\",\\"email_address\\":\\"never@again.com\\"}]}]}"')
        
        # Test authorized access with different user 
        client.logout()
        client.login(username='aliteralshirt', password='button')
        response = client.get('/mailing_campaign/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'"{\\"contact_lists\\":[]}"')
        
    
    def test_create_campaign(self):
        client = Client()
        with open('mailing_campaign/examples/mail_test.json') as campaign:
            campaign_json = campaign.read()

            # Test unauthorized access
            response = client.post('/start_campaign/', campaign_json, content_type='application/json')
            self.assertEqual(response.status_code, 401)
            client.login(username='aliteralshoe', password='lace')

            # Test response for non-existent video
            response = client.post('/start_campaign/', campaign_json, content_type='application/json')
            self.assertEqual(response.status_code, 400)
            Video.objects.create(user=User.objects.get(username='aliteralshoe'))
            
            # Check if video exists
            self.assertEqual(f'{Video.objects.all()}', '<QuerySet [<Video: Video object (1)>]>')
        
            # Test response for non-existent contact list
            response = client.post('/start_campaign/', campaign_json, content_type='application/json')
            self.assertEqual(response.status_code, 400)
            
            with open('mailing_campaign/examples/test.json') as contact_list:
                contact_list_json = contact_list.read()
                client.post('/mailing_campaign/', contact_list_json, content_type='application/json')
                client.post('/mailing_campaign/', contact_list_json, content_type='application/json')

            # Test proper functionality
            response = client.post('/start_campaign/', campaign_json, content_type='application/json')
            self.assertEqual(response.status_code, 201)
    
    @staticmethod
    def create_campaign_dict():
        return {'video_id' : 1, 'template_id' : 10, 'contact_list_id' : 2}

    def test_campaign_post_serializer(self):
        client = Client()
        client.login(username='aliteralshoe', password='lace')
        video = Video.objects.create(user=User.objects.get(username='aliteralshoe'))
        with open('mailing_campaign/examples/test.json') as contact_list:
            contact_list_json = contact_list.read()
            client.post('/mailing_campaign/', contact_list_json, content_type='application/json')
            client.post('/mailing_campaign/', contact_list_json, content_type='application/json')
        
        serializer = CampaignSerializer(data=self.create_campaign_dict())
        self.assertTrue(serializer.is_valid())

        campaign = Campaign(1, 10, 2)
        campaign.video = video
        campaign.contact_list = ContactList.objects.get(id=2)
        campaign_post = CampaignPost(campaign.template_id,
                                     generate_instances(campaign))
        post_serializer = CampaignPostSerializer(campaign_post)
        rendered = JSONRenderer().render(post_serializer.data)
        self.assertEqual(rendered, b'{"template_id":10,"instances":[{"email_address":"for@ever.de","data":{"first_name":"For","last_name":"Ever","video_link":""}},{"email_address":"never@again.com","data":{"first_name":"Never","last_name":"Again","video_link":""}}]}')
