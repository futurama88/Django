from datetime import datetime
from celery import shared_task
import datetime
from django.template.loader import render_to_string
from NEWS.models import Post, Category
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


@shared_task
def send_email_task(preview, pk, title, instance, subscribers):
    categories = instance.postCategory.all()
    subscribers_emails = []
    for cat in categories:
        subscribers = cat.subscribers.all()
        subscribers_emails += [s.email for s in subscribers]
        send_email_task(instance.preview(), instance.pk, instance.title, subscribers_emails)

    html_content = render_to_string(
        'cost_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }

    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

#
@shared_task
def weekly_send_email_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dataCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    print(subscribers)

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
