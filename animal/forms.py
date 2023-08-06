from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from .models import *


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категорію не вибрано'  # міняємо властивість форми при створенні

    class Meta:
        model = Animal
        fields = ['title', 'content', 'photo', 'is_published', 'cat']

        widgets = {
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Довжина перевищує 200 символів')
        return title


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    ava = forms.FileField(label='Аватарка', required=False)

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password1', 'password2', 'ava')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder':'Username'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder':'Password'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Ім\'я', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField(label='Капча')


class Profile(forms.ModelForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input-prof'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input-prof'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input-prof'}))
    first_name = forms.CharField(label='Ім\'я',required=False, widget=forms.TextInput(attrs={'class': 'form-input-prof'}))
    last_name = forms.CharField(label='Прізвище',required=False, widget=forms.TextInput(attrs={'class': 'form-input-prof'}))
    ava = forms.FileField(required=False, label='Загрузка файлу')

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password1', 'first_name', 'last_name', 'ava')


# Переоприділяємо аргумент класу щоб можна було не зберігати фото
class UpdateAddPostForm(AddPostForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = False