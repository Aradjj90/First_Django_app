from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    ava = models.BinaryField(blank=True, null=True, editable=True)


class Animal(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Контент')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Час створення')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Час редагування')
    is_published = models.BooleanField(default=True, verbose_name='Публіковано')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категорії')
    owner = models.CharField('Owner', max_length=255, blank=True, default="root")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name ='Тварини' # Переназвали імя таблиці в адмін панелі
        verbose_name_plural = 'Тварини' # Переназвали імя таблиці в адмін панелі для множинних значень
        ordering = ['-time_create', 'title'] # сортування по часу створення, а потім по назві. Так само сортує і на сторінці сайту


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категорія')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name ='Категорії'
        verbose_name_plural = 'Категорії'
        ordering = ['id']