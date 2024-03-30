from django.urls import path

from post.views import PostListView, PostDetailView, PostCreateView, \
    PostUpdateView, PostDeleteView

app_name = 'post'
urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('posts/<int:id>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/new/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:id>/update/', PostUpdateView.as_view(), name='post_edit'),
    path('posts/<int:id>/delete/', PostDeleteView.as_view(), name='post_delete'),
]