from django.core.mail import EmailMultiAlternatives
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User
from django import forms

from .models import Post
from NewsPortal import settings


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'post_type',
            'post_category',
            'post_header',
            'post_text',
        ]


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name="common")
        basic_group.user_set.add(user)
        mail = (User.objects.get(username=user).email,)

        msg = EmailMultiAlternatives(
            subject='Регистрация на сайте NewsPortal',
            body='Здраствуйте, регистрация прошла успешно',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=mail,
        )
        msg.send()
        return user
