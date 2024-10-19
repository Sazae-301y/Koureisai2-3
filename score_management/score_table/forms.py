from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['comment']  # slugフィールドは削除
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'コメントを入力してください'}),
        }