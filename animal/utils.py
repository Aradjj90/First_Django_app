from _datetime import datetime
from animal.models import *

menu = [
      {'title': 'Зворотній зв\'язок', 'url_name': 'contact'},
      {'title': 'Добавити статтю', 'url_name': 'add_page'},
      {'title': 'Допоможи вр\'ятувати', 'url_name': 'world_animal'},
      ]


class DataMixin:
    def get_user_context(self, flag=True, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = cats
        context['year'] = datetime.now().year
        if 'cat_selected' not in context and flag:
            context['cat_selected'] = 0
        return context
