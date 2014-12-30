import datetime
from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse
from rango.models import Category,Page

def add_cat(name,views,likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

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

class PageMethodTests(TestCase):
    def test_first_visit_on_the_future(self):
     """
        first_visit_on_the_future validate that when we add a page the field first_visit is not in the future

     """
     futuretime = timezone.now() + datetime.timedelta(days=2)
     c,_ = Category.objects.get_or_create(name='CategoryTest')
     p = c.page_set.create(title = 'Wikipedia', url= 'htttp://wikipedia.org',views=0,first_visit=futuretime,last_visit=timezone.now())
     p.save()
     self.assertEqual(p.first_visit >= timezone.now(),False)

    def test_last_visit_on_the_future(self):
     """
        last_visit_on_the_future validate that when we add a page the field first_visit is not in the future

     """
     futuretime = timezone.now() + datetime.timedelta(days=2)
     c,_ = Category.objects.get_or_create(name='CategoryTest')
     p = c.page_set.create(title = 'Wikipedia', url= 'htttp://wikipedia.org',views=0,first_visit=timezone.now(),last_visit=futuretime)
     p.save()
     self.assertEqual(p.last_visit >= timezone.now(),False)

    def test_last_visit_greater_than_first_visit(self):
     """
        llast_visit_greater_than_first_visit validate that when we add a page the field last_visit is greater than or equal to the field first_visit

     """
     futuretime = timezone.now() + datetime.timedelta(days=2)
     c,_ = Category.objects.get_or_create(name='CategoryTest')
     p = c.page_set.create(title = 'Wikipedia', url= 'htttp://wikipedia.org',views=0,first_visit=futuretime,last_visit=timezone.now())
     p.save()
     self.assertEqual(p.last_visit >= p.first_visit,True)




class IndexViewTest(TestCase):
    def test_index_view_with_no_categories(self):
        """
        if no question exist, an appropiate message should be displayed

        """

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"There are no categories in this moment.")
        self.assertQuerysetEqual(response.context['categories'],[])



    def test_index_view_with_categories(self):
        """
        test the categories existence

        """

        add_cat('test1',1,1)
        add_cat('test2',1,1)
        add_cat('test3',1,1)
        add_cat('test4',1,1)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"test4")

        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats,4)














