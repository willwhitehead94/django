from django.contrib import admin
from .models import Post, Comment


# Register your models here.
@admin.register(Post)  # admin.site.register(Post) is replaced by the decorator
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')  # The elements to display in the list.
    list_filter = ('status', 'created', 'publish', 'author')  # The elements that can be filtered by.
    search_fields = ('title', 'body')  # Shows a search bar that will search the  given fields.
    date_hierarchy = 'publish'  # Shows a hierachy just below search box based on given field.
    ordering = ('status', 'publish')  # Order of elements shown in panel.
    prepopulated_fields = {'slug': ('title',)}  # Told Django to fill in the left element with the value on the right of the dict.
    raw_id_fields = ('author', )  # Makes Django to build a lookup function.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')