from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.utils import timezone
from Home.models import DiaryEntry, Tag
from Home.components.dashboard import DashboardView

class DashboardComponentTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.request = self.factory.get('/')
        self.request.user = self.user

        # Create tag
        self.tag_happy = Tag.objects.create(name='happy')
        self.tag_reflection = Tag.objects.create(name='reflection')

        # Create some diary entries
        self.entry1 = DiaryEntry.objects.create(
            user=self.user,
            title='Amazing Day',
            content='Today was a wonderful and happy day in the park.',
            mood='happy',
            created_at=timezone.now(),
            favorite=True
        )
        self.entry1.tags.add(self.tag_happy)

        self.entry2 = DiaryEntry.objects.create(
            user=self.user,
            title='Calm Evening',
            content='A peaceful reflection on today\'s events.',
            mood='calm',
            created_at=timezone.now(),
            favorite=False
        )
        self.entry2.tags.add(self.tag_reflection)

    def test_stats_calculation(self):
        component = DashboardView(component_name='dashboard', id='test-dashboard-id')
        component.request = self.request

        stats = component.get_stats()
        self.assertEqual(stats['total_entries'], 2)
        self.assertEqual(stats['favorite_entries'], 1)
        self.assertEqual(stats['this_month'], 2)
        # Verify mood and tag display
        self.assertIn('Happy', stats['most_used_mood'])
        # Since tags are annotated by count, happy and reflection have same counts (1 each), so either could be returned.
        self.assertIn(stats['most_used_tag'], ['happy', 'reflection'])

    def test_search_by_title(self):
        component = DashboardView(component_name='dashboard', id='test-dashboard-id')
        component.request = self.request
        
        component.search_query = 'Amazing'
        entries = list(component.get_entries())
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].id, self.entry1.id)

    def test_search_by_content(self):
        component = DashboardView(component_name='dashboard', id='test-dashboard-id')
        component.request = self.request
        
        component.search_query = 'peaceful'
        entries = list(component.get_entries())
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].id, self.entry2.id)

    def test_search_by_tag(self):
        component = DashboardView(component_name='dashboard', id='test-dashboard-id')
        component.request = self.request
        
        component.search_query = 'reflection'
        entries = list(component.get_entries())
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].id, self.entry2.id)

    def test_favorites_only_filter(self):
        component = DashboardView(component_name='dashboard', id='test-dashboard-id')
        component.request = self.request
        
        component.show_only_favorites = True
        entries = list(component.get_entries())
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].id, self.entry1.id)

    def test_toggle_favorite_action(self):
        component = DashboardView(component_name='dashboard', id='test-dashboard-id')
        component.request = self.request
        
        # entry2 is currently not favorited
        self.assertFalse(self.entry2.favorite)
        component.toggle_favorite(self.entry2.id)
        
        # Refresh and verify
        self.entry2.refresh_from_db()
        self.assertTrue(self.entry2.favorite)

    def test_delete_entry_action(self):
        component = DashboardView(component_name='dashboard', id='test-dashboard-id')
        component.request = self.request
        
        # Confirm delete id
        component.confirm_delete(self.entry2.id)
        self.assertEqual(component.confirm_delete_id, self.entry2.id)
        
        # Cancel delete id
        component.cancel_delete()
        self.assertIsNone(component.confirm_delete_id)
        
        # Confirm again and delete
        component.confirm_delete(self.entry2.id)
        component.delete_entry(self.entry2.id)
        
        # Check DB
        self.assertFalse(DiaryEntry.objects.filter(id=self.entry2.id).exists())
