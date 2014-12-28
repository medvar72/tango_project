from django.test import TestCase
from rango.models import Category

class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """
        ensure_views_are_positive should results True for Categories where views are zero or positive

        """
        cat = Category(name="test",views=-1,likes=0)
        cat.save()
        self.assertEqual((cat.views>=0),True)

    def test_slug_line_creation(self):
        """
        slug_line_creation checks to make sure that when we add a category an appropiate slug line is created
        i.e "Random Category String --> random-category-string"

        """
        # cat = Category(name='test',slug='Random Category String')
        cat = Category(name = 'Random Category String', views = 0, likes = 0)
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')




