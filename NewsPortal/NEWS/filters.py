from django_filters import FilterSet, ModelChoiceFilter

from .models import Post, Category


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    Categorytype = ModelChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),  # название класса в models.py
        label='категория',
        empty_label='любой',
    )

    PostTitle = ModelChoiceFilter(
        field_name='title',
        queryset=Post.objects.all(),  # название класса в models.py
        label='заголовок',

    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'title': ['icontains'],
            # количество товаров должно быть больше или равно
            'dataCreation': ['day'],
            # 'title': ['exact'],

        }
