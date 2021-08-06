from django.test import TestCase
from rango.models import Category, UserProfile, Page
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class CategoryModelTests(TestCase): # Test Models
    def test_slug_line_creation(self):
        category = Category(name='Random Category String')
        category.save()
        self.assertEqual(category.slug, 'random-category-string')

class UserProfileModelTests(TestCase): 
    def test_ensure_username_is_valid(self):
        user = User(username='Tom')
        user.save()
        userProfile = UserProfile()
        userProfile.user = user
        userProfile.save()
        self.assertIsNot(userProfile.user.username, '')
        self.assertIsNotNone(userProfile.user.username)

class IndexViewTests(TestCase): # Test Views
    def test_index_view_with_no_categories(self):
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no categories present.')
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        """
        Checks whether categories are displayed correctly when present.
        """
        add_category('Python', 1, 1)
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python")
        num_categories = len(response.context['categories'])
        self.assertEquals(num_categories, 1)
    
    def test_index_view_has_Welcome(self):
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to Rango')

class PageViewTests(TestCase):
    def test_page_view_title(self):
        page = Page()
        page.title = 'a'
        response = self.client.get(reverse('rango:show_page', kwargs={'page_name_slug': 'a'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'a')

def add_category(name, views=0, likes=0):
    category = Category.objects.get_or_create(name=name)[0]
    category.views = views
    category.likes = likes
    category.save()
    return category
