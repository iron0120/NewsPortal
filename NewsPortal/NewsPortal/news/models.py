from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    user_author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rat = self.post_set.aggregate(post_r=Sum('post_rating'))
        p_rat = 0
        p_rat += post_rat.get('post_r')

        comm_rat = self.user_author.comment_set.aggregate(comm_r=Sum('comment_rating'))
        c_rat = 0
        c_rat += comm_rat.get('comm_r')

        self.author_rating = p_rat * 3 + c_rat
        self.save()

    def __str__(self):
        return self.user_author.username


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True, )
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.category


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    CATEGORY = [(ARTICLE, 'статья'),
                (NEWS, 'новость')
                ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=CATEGORY, default=ARTICLE)
    post_add_time = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_header = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return '{}...'.format(self.post_text[:124])

    def get_absolute_url(self):
        return reverse('news', args=[str(self.id)])

    def __str__(self):
        return self.post_header

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'news-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_time_add = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return self.comment_text
