from django.contrib import admin
from .models import Post, Comment, Category

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'date_posted',)
    list_display_links = ('id', 'title',)
    list_filter = ['date_posted']
    search_fields = ['title']


admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'content', 'user', 'date_posted')

admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
