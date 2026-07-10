from django_unicorn.components import UnicornView
from Home.models import DiaryEntry, Tag
from django.db.models import Q, Count
from django.utils import timezone
from django.core.paginator import Paginator

class DashboardView(UnicornView):
    search_query = ""
    show_only_favorites = False
    page_number = 1
    confirm_delete_id = None
    entries_per_page = 6

    def updated_search_query(self, query):
        self.page_number = 1

    def toggle_show_only_favorites(self):
        self.show_only_favorites = not self.show_only_favorites
        self.page_number = 1

    def get_entries(self):
        user = self.request.user
        if not user.is_authenticated:
            return DiaryEntry.objects.none()
        
        entries = DiaryEntry.objects.filter(user=user)
        if self.show_only_favorites:
            entries = entries.filter(favorite=True)
            
        if self.search_query:
            entries = entries.filter(
                Q(title__icontains=self.search_query) |
                Q(content__icontains=self.search_query) |
                Q(tags__name__icontains=self.search_query)
            ).distinct()
        return entries

    def get_context_data(self):
        return {
            'stats': self.get_stats(),
            'paginated_entries': self.get_paginated_entries()
        }

    def get_paginated_entries(self):
        entries = self.get_entries()
        paginator = Paginator(entries, self.entries_per_page)
        page_obj = paginator.get_page(self.page_number)
        return page_obj

    def get_stats(self):
        user = self.request.user
        if not user.is_authenticated:
            return {
                'total_entries': 0,
                'favorite_entries': 0,
                'this_month': 0,
                'most_used_mood': 'None',
                'most_used_tag': 'None'
            }
        
        user_entries = DiaryEntry.objects.filter(user=user)
        total_entries = user_entries.count()
        favorite_entries = user_entries.filter(favorite=True).count()
        
        now = timezone.now()
        this_month = user_entries.filter(created_at__year=now.year, created_at__month=now.month).count()
        
        # Most used mood
        mood_counts = user_entries.values('mood').annotate(count=Count('mood')).order_by('-count')
        if mood_counts:
            most_used_mood = mood_counts[0]['mood']
            mood_map = dict(DiaryEntry.MOOD_CHOICES)
            most_used_mood_display = mood_map.get(most_used_mood, most_used_mood)
        else:
            most_used_mood_display = "None"
            
        # Most used tag
        tag_counts = Tag.objects.filter(entries__user=user).annotate(count=Count('entries')).order_by('-count')
        if tag_counts:
            most_used_tag = tag_counts[0].name
        else:
            most_used_tag = "None"
            
        return {
            'total_entries': total_entries,
            'favorite_entries': favorite_entries,
            'this_month': this_month,
            'most_used_mood': most_used_mood_display,
            'most_used_tag': most_used_tag
        }

    def toggle_favorite(self, entry_id):
        try:
            entry = DiaryEntry.objects.get(id=entry_id, user=self.request.user)
            entry.favorite = not entry.favorite
            entry.save()
        except DiaryEntry.DoesNotExist:
            pass

    def confirm_delete(self, entry_id):
        self.confirm_delete_id = entry_id

    def cancel_delete(self):
        self.confirm_delete_id = None

    def delete_entry(self, entry_id):
        try:
            entry = DiaryEntry.objects.get(id=entry_id, user=self.request.user)
            entry.delete()
            self.confirm_delete_id = None
            
            # Recalculate pagination page number if the current page became empty
            entries = self.get_entries()
            paginator = Paginator(entries, self.entries_per_page)
            if self.page_number > paginator.num_pages and paginator.num_pages > 0:
                self.page_number = paginator.num_pages
        except DiaryEntry.DoesNotExist:
            pass

    def set_page(self, page):
        self.page_number = int(page)
