from django.test import TestCase
from django.urls import reverse

class RecipeURLSTest(TestCase):
    def test_the_test_is_ok(self):
        assert 1 == 1, 'One equals one'

    def test_recipe_home_url_is_correct(self):
        home_url = reverse('recipes-home')
        self.assertEqual(home_url, '/')