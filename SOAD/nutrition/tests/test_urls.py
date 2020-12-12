from django.urls import reverse, resolve

class TestUrls:

    def test_water_url(self):
        path = reverse('water')
        assert resolve(path).view_name == 'water'

    def test_sleep_url(self):
        path = reverse('sleep')
        assert resolve(path).view_name == 'sleep'

    def test_calorie_url(self):
        path = reverse('calorie')
        assert resolve(path).view_name == 'calorie'
    