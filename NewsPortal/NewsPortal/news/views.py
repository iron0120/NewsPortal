import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import *
from .filters import PostFilter


class PostList(ListView):
    logger = logging.getLogger(__name__)
    model = Post
    ordering = '-post_add_time'
    template_name = 'all_news.html'
    context_object_name = 'all_news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# class NewsSearch(ListView):
#     model = Post
#     template_name = 'search.html'
#     context_object_name = 'all_news'
#     ordering = '-post_add_time'
#     paginate_by = 2


class PostDetail(DetailView):
    logger = logging.getLogger(__name__)
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'news-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'news-{self.kwargs["pk"]}', obj)
        return obj


class NewsCreate(PermissionRequiredMixin, CreateView):
    logger = logging.getLogger(__name__)
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class NewsEdit(PermissionRequiredMixin, UpdateView):
    logger = logging.getLogger(__name__)
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    logger = logging.getLogger(__name__)
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('all_news')


class CategoryListView(ListView):
    logger = logging.getLogger(__name__)
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        self.post_category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.post_category).order_by('-post_add_time')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.post_category.subscribers.all()
        context['category'] = self.post_category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})
