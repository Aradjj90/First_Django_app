import os
import random
from base64 import b64encode

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from django.shortcuts import redirect, render

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from transliterate import slugify as slugify_ua
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib import messages

from .utils import *
from .forms import *


class AnimalHome(DataMixin, ListView):
    paginate_by = 2
    model = Animal
    template_name = 'animal/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Головна сторінка")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Animal.objects.filter(is_published=True)


class ShowPost(DataMixin, DetailView):
    model = Animal
    template_name = 'animal/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class AnimalCategory(DataMixin, ListView):
    model = Animal
    template_name = 'animal/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категорії - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Animal.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'animal/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Додавання статті", update_flag=False)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        owner = form.save(commit=False)
        owner.owner = self.request.user.username
        owner.slug = slugify_ua(owner.title)
        if owner.slug is None:
            owner.slug = slugify(owner.title)
        owner.save()
        return redirect('home')


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'animal/contact.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Зворотний зв\'язок')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'animal/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регістрація")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save(commit=False)
        binary = user.ava
        if binary is None:
            binary = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                       'animal/static/animal/images/ava/' + str(random.randint(1, 30)) + '.png'), 'rb')
        user.ava = binary.read()
        user.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'animal/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):  #
        context = super().get_context_data(**kwargs)  # бере контекст який вже існує
        c_def = self.get_user_context(title="Авторизація")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    cats = Category.objects.all()
    posts = Animal.objects.filter(owner=request.user)
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(1)

    if request.method == "POST":
        form = Profile(request.POST or None, request.FILES or None, instance=request.user)
        checksize = request.FILES.get('ava')
        if checksize is not None:
            print('зайшло')
            if checksize.size > 512 * 512:
                messages.error(request, "Фото завелике")
                return render(request, 'animal/profile.html',
                              {'menu': user_menu,
                               'form': form,
                               'cats': cats,
                               'year': datetime.now().year,
                               'title': 'Профіль користувача: ',
                               })

            if form.is_valid():
                f = form.save(commit=False)
                binary = f.ava
                f.ava = binary.read()
                f.save()
                return redirect('profile')
        else:
            if form.is_valid():
                form.save()
                return redirect('profile')

    else:
        ava_encoded = b64encode(request.user.ava).decode('ascii')
        form = Profile(request.POST or None, instance=request.user)
        return render(request, 'animal/profile.html',
                      {'menu': user_menu,
                       'form': form,
                       'cats': cats,
                       'posts': posts,
                       'year': datetime.now().year,
                       'ava': ava_encoded,
                       'title': 'Профіль користувача: ',
                       })


def safe_animal(request):
    return redirect("https://www.worldanimalprotection.org/")


class YourPost(LoginRequiredMixin, DataMixin, ListView):
    model = Animal
    template_name = 'animal/index.html'
    context_object_name = 'posts'
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Твої пости", your_posts=True)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Animal.objects.filter(owner=self.request.user.username)


def search(request):
    cats = Category.objects.all()
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(1)

    if request.method == "POST":
        searched = request.POST['searched']
        posts = Animal.objects.filter(content__icontains=searched, is_published=True)# istartswith, icontains
        return render(request, 'animal/search.html',
                      {'menu': user_menu,
                       'cats': cats,
                       'posts': posts,
                       'year': datetime.now().year,
                       'searched': searched,
                       'title': 'Профіль користувача:',
                       })
    else:
        return render(request, 'animal/search.html',
                      {'menu': user_menu,
                       'cats': cats,
                       'year': datetime.now().year,
                       'title': 'Профіль користувача:',
                       })


@login_required
def update_post(request, post_slug):
    post_info = Animal.objects.get(slug=post_slug)
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(1)
    update_flag = True
    if request.method == "POST":
        form = UpdateAddPostForm(request.POST or None, request.FILES or None, instance=post_info)
        if form.is_valid():
            form.save()
            return redirect(post_info.get_absolute_url())
    else:
        form = UpdateAddPostForm(request.POST or None, instance=post_info)
        return render(request, 'animal/addpage.html',
                      {'menu': user_menu,
                       'form': form,
                       'post_info': post_info,
                       'update_flag': update_flag,
                       'year': datetime.now().year,
                       'title': 'Оновлення поста',
                       })


@login_required
def delete_post(request, post_slug):
    post = Animal.objects.get(slug=post_slug)
    post.delete()
    messages.success(request, f"Пост \"{post}\" видалено")
    return redirect('home')


