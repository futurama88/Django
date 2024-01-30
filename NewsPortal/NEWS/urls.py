from django.urls import path
# Импортируем созданное нами представление
from .views import (PostView, PostCategoryView, CommentView, ArticleView, SearchView, create_post,
                    PostUpdate, PostDelete, PostCreate, subscriptions)
from django.views.decorators.cache import cache_page


urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', PostView.as_view(), name='post_list'),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('<int:pk>',cache_page(60)(PostCategoryView.as_view())),
    path('comment/<int:pk>', CommentView.as_view()),
    path('article/<int:pk>', ArticleView.as_view()),
    path('search/', SearchView.as_view()),
    path('createfunc/', create_post),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('post/<int:pk>/', PostView.as_view(), name='post_detail'),
    path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('subscriptions/', subscriptions, name='subscriptions'),
   
]
