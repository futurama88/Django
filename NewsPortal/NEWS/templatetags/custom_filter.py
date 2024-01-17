from django import template

register = template.Library()


# Регистрируем наш фильтр под именем censor, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
# Декоратор register.filter() указывает Django, что нужно запомнить про существование нового фильтра.
@register.filter()
def censor(text: str):
    """
   text: строка, к которой нужно применить фильтр
   """

    censor_list = [
        'nigga',
        'уничтожение',
        'сражением',
    ]

    if isinstance(text, str):
        text_list = text.split(' ')
        # т.к. мы имеем абзац текста нам надо разбить его на слова чтобы проитерировать и найти там бранное слово

        for i, word in enumerate(text_list):
            # Если range() позволяет получить только индексы элементов списка, то enumerate() – сразу индекс элемента
            # и его значение. i - это индекс списка, word - значение
            if word in censor_list:
                text_list[i] = 'брань'.join([word[0], '*' * (len(word) - 1)])
                # если слово в бранном списке, то к первой букве слова пррибавляем "брань" и количество
                # звезд=количечтву букв
    else:
        raise KeyError('Введена не строка')

    return ' '.join(text_list)
