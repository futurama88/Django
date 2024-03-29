import logging
from datetime import datetime

import permission as permission
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import PostFilter
from .forms import PostForm
from .serializers import ArticleSerializer

logger = logging.getLogger(__name__)

from django.utils import timezone

from django.shortcuts import redirect

import pytz

from django.shortcuts import render
from rest_framework import viewsets


from NEWS.models import *
from rest_framework.response import Response


# @cache_page(60)  # в аргументы к декоратору передаём количество секунд,
# которые хотим, чтобы страница держалась в кэше.
# Внимание! Пока страница находится в кэше, изменения,
# происходящие на ней, учитываться не будут!
# def create_post(request):
#     form = PostForm()
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/news/')
#
#     return render(request, 'post_edit.html', {'form': form})

#
@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


class Index(View):
    def get(self, request):
        models = Post.objects.all()

        context = {
            'models': models
        }

        return HttpResponse(render(request, 'language.html', context))


class PostView(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post

    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dataCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 6  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filterset = None

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)

        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/news/')

    # def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
    #     obj = cache.get(f'post-{self.kwargs["pk"]}',
    #                     None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.
    #
    #     if not obj:
    #         obj = super().get_object(queryset=self.queryset)
    #         cache.set(f'post-{self.kwargs["pk"]}', obj)
    #         return obj
    #


class SearchView(ListView):
    model = Post
    ordering = '-dataCreation'
    template_name = 'search.html'
    context_object_name = 'search'
    filter_class = PostFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)

        return self.filterset.qs.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset

        return context


class PostCategoryView(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'posts.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post_detail'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post_detail-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post_detail-{self.kwargs["pk"]}', obj)
        return obj


class CommentView(DetailView):
    model = Comment
    ordering = '-dateCreation'
    template_name = 'comment.html'
    context_object_name = 'comment'


class ArticleView(DetailView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dataCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'article.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'article'


# Добавляем новое представление для создания товаров.
class PostCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('NEWS.add_post',)
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'
    success_url = '/news/'


# Добавляем представление для изменения товара.
class PostUpdate(UpdateView):
    permission_required = ('NEWS.change_product',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = '/news/'


# Представление удаляющее товар.
class PostDelete(DeleteView):
    permission_required = ('NEWS.delete_product',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryListView(PostView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-dataCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['postCategory'] = self.postCategory
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    postCategory = Category.objects.get(id=pk)
    postCategory.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории '
    return render(request, 'subscribe.html', {'postCategory': postCategory, 'message': message})


# class IndexView(View):
#     def get(self, request):
#         printer.apply_async([10],
#                             eta=datetime.now() + timedelta(seconds=5))
#         hello.delay()
#         return HttpResponse('Hello!')


class ArticleViewset(viewsets.ModelViewSet):
    queryset = Post.objects.filter(categoryType='AR')
    serializer_class = ArticleSerializer


 
