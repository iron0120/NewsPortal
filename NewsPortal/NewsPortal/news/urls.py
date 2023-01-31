from django.urls import path
from django.views.decorators.cache import cache_page

from .views import PostList, PostDetail, NewsCreate, NewsEdit, NewsDelete, CategoryListView, subscribe

urlpatterns = [
   path('', PostList.as_view(), name='all_news'),
   path('<int:pk>', cache_page(60*10)(PostDetail.as_view()), name='news'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   # path('become/', become_author, name='become_author'),
]
