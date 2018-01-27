from django.contrib import admin
from restAPI.models import Post, Tag, Comment, Reply


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'pub_time', 'title', 'excerpt')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'pub_time', 'body', 'post')


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'pub_time', 'body', 'post', 'comment')


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)
