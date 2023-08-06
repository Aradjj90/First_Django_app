from django.contrib import admin

from .models import *


# Класи для відображення полів таблиць в Адмін панелі
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create') # в адмінці появляється сайт бар з пошуковими фільтрами
    prepopulated_fields = {"slug": ("title",)}  # формує поле 'slug' на основі поля 'name'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)} # формує поле 'slug' на основі поля 'name'


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', )


admin.site.register(Animal, AnimalAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MyUser, MyUserAdmin)