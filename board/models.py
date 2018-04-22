from django.db import models

from django.utils import timezone
import datetime


class Category(models.Model):
    name = models.CharField('Category', max_length=20)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_latest_post(self):
        return Post.objects.filter(category=self).order_by('-date_posted')


class Post(models.Model):
    title = models.CharField('Post title', max_length=50)
    content = models.CharField('Content', max_length=1000)
    user = models.CharField('User', max_length=20)
    date_posted = models.DateTimeField('Date posted')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField('Content', max_length=1000)
    user = models.CharField('User', max_length=20)
    date_posted = models.DateTimeField('Date posted')

    def __str__(self):
        return self.content

    @property
    def was_recently_added(self):
        return self.date_posted > timezone.now() - datetime.timedelta(days=1)