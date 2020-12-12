from django.test import SimpleTestCase
from django.urls import reverse, resolve
from advertise.views import fitnessproduct_list_view, fitnessproduct_detail_view

class TestUrls(SimpleTestCase):
    def test_list_url_resolves(self):
        url = reverse('fitness-product-list')
        self.assertEquals(resolve(url).func, fitnessproduct_list_view)
    
    def test_fp_detail_url_resolves(self):
        url = reverse('fitnessproduct_detail', args=['some-slug'])
        self.assertEquals(resolve(url).func, fitnessproduct_detail_view)