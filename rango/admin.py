from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile, Comment

# Register your models here.

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')
    prepopulated_fields = {'slug':('title',)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'writtenTime', 'content', 'page')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
admin.site.register(Comment, CommentAdmin)

