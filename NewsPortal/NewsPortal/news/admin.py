from django.contrib import admin

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_header', 'author', 'post_type', 'post_rating')
    list_filter = ('author', 'post_rating')
    search_fields = ('author', )


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
