from django import forms
from .models import DiaryEntry, Tag

class DiaryEntryForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        label="Tags",
        help_text="Separate tags with commas (e.g. happy, travel, reflection)",
        widget=forms.TextInput(attrs={'placeholder': 'happy, travel, reflection', 'class': 'form-control'})
    )

    class Meta:
        model = DiaryEntry
        fields = ['title', 'content', 'mood']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Write your thoughts...', 'class': 'form-control'}),
            'mood': forms.Select(attrs={'class': 'form-select'}),
        }

    def save(self, commit=True, user=None):
        entry = super().save(commit=False)
        if user:
            entry.user = user
        if commit:
            entry.save()
            # Process and clean tag strings
            tags_str = self.cleaned_data.get('tags_input', '')
            entry.tags.clear()
            if tags_str:
                tag_names = [name.strip().lower() for name in tags_str.split(',') if name.strip()]
                for name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=name)
                    entry.tags.add(tag)
        return entry
