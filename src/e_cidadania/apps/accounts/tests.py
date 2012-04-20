from django.test import TestCase
from django.core.urlresolvers import reverse
<<<<<<< HEAD

class Get_Test(TestCase):
    fixtures = ['temp2.json']
    
    def test_index(self):
        response = self.client.get('/accounts/')
        self.assertEqual(response.status_code, 302)
        print response
=======
from e_cidadania.apps.debate.models import Debate, Note, Row, Column
from django.contrib.auth.models import User, Group
from django.shortcuts import render_to_response, get_object_or_404, redirect
from e_cidadania.apps.spaces.models import Space, Entity, Document, Event, Intent
from e_cidadania.apps.userprofile.models import BaseProfile
from e_cidadania.apps.accounts.models import UserProfile, Interest


class Get_Test(TestCase):
    fixtures = ['1.json']
    #fixtures = ['temp1.json']
    
    def setUp(self):
        super(Get_Test, self).setUp()
        self.u1 = UserProfile.objects.get(pk=1)
        self.u2 = UserProfile.objects.get(pk=2)
        self.s = UserProfile.objects.get(pk=1).spaces
    def test1(self):
        print self.u1.pk
        print self.u2.pk
        print self.u1.surname
        print self.u1.firstname
        self.a = self.u1.spaces
        print self.a.objects.all() 
        
>>>>>>> testing2
        

