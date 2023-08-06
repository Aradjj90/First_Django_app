from django.urls import path

from .views import *

urlpatterns = [
    path('', AnimalHome.as_view(), name='home'),
    path('add_page/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_user, name='logout'),
    path('world_animal/', safe_animal, name='world_animal'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', AnimalCategory.as_view(), name='category'),
    path('search/', search, name='search_post'),
    path('your_post/', YourPost.as_view(), name='your_post'),
    path('update_post/<slug:post_slug>/', update_post, name='update_post'),
    path('delete_post/<slug:post_slug>/', delete_post, name='delete_post'),

]


