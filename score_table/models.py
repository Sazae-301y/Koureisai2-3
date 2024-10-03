from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string

class Post(models.Model):
    comment = models.TextField()
    slug = models.SlugField(unique=True, blank=True)  # blank=Trueでフォーム上の入力を不要に
    posted_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # If the slug is empty, auto-generate it
            post_count = Post.objects.count() + 1  # Get the total number of posts
            base_slug = f"Post{post_count}"  # Use the post count as the base slug
            unique_slug = base_slug
            while Post.objects.filter(slug=unique_slug).exists():  # Ensure uniqueness
                unique_slug = f"{base_slug}-{get_random_string(5)}"  # Add random string if not unique
            self.slug = unique_slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.slug}: {self.comment[:20]}"

class Participant(models.Model):
    nickname = models.CharField(max_length=100)
    score = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname
    
class FujitaRanking(models.Model):
    participant = models.CharField(max_length=100)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.participant}: {self.score}'