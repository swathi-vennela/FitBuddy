from django.test import TestCase, Client
from django.urls import reverse
from fitbuddy.models import *
import json

class TestViews(TestCase):

    def test_hiring_list(self):
        # client = Client()
        response = self.client.get(reverse('list_hiring_roles'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fitbuddy/hiring_list.html')
