from django.test import TestCase
from django.core.urlresolvers import reverse
from e_cidadania.apps.debate.models import Debate, Note, Row, Column
from django.contrib.auth.models import User, Group
from django.shortcuts import render_to_response, get_object_or_404, redirect
from e_cidadania.apps.spaces.models import Space, Entity, Document, Event, Intent

class Get_Test(TestCase):
    fixtures = ['1.json']
    
    def test_index(self):
        response = self.client.get('/debate/')
        print Debate.objects.all()
        a = Debate.objects.all()
        
        
        last_debate_id = Debate.objects.latest('id')
        current_debate_id = last_debate_id.pk
        print current_debate_id
        
        #print last_debate_id
        
        debate_instance = get_object_or_404(Debate, pk=current_debate_id)
        
        #.filter(space=place.id)
        
        
        
        
        objects = Debate.objects.all().filter(space=1)
        print objects
        
        objects = Debate.objects.all().filter(space=2)
        print objects
        
        objects = Debate.objects.all().filter(space=3)
        print objects
        
        
        
        
        
        
