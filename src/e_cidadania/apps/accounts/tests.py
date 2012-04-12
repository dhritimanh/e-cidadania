from django.test import TestCase
from django.core.urlresolvers import reverse

class Get_Test(TestCase):
    fixtures = ['temp2.json']
    
    def test_index(self):
        response = self.client.get('/accounts/')
        self.assertEqual(response.status_code, 302)
        print response
        

