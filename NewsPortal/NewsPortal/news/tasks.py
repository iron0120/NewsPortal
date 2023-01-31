import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPortal import settings
from news.models import Category, Post

today = datetime.datetime.now()
last_week = today - datetime.timedelta(days=7)
posts = Post.objects.filter(post_add_time__gte=last_week)
categories = posts.values_list('post_category__category', flat=True)
subscribers = set(Category.objects.filter(category__in=categories).values_list('subscribers__email', flat=True))


@shared_task()
def notify_subscribers_about_weekly_news():
    htm_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts
        }
    )

    msg = EmailMultiAlternatives(
        subject='Сатьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(htm_content, 'text/html')
    msg.send()


@shared_task()
def send_notifications(preview, pk, post_header):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=post_header,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

