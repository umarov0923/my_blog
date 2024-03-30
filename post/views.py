from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import View, UpdateView, DeleteView

from post.forms import PostForm, CommentForm
from post.models import Post, Tag


class PostListView(View):
    def get(self, request):
        search_post = request.GET.get('search', '')
        posts = Post.objects.filter(is_published=True)
        latest_posts = posts.order_by('-created_time')[:5]
        most_viewed_posts = posts.filter(is_published=True).order_by('-views')[:5]
        week_popular_posts = posts.filter(created_time__gte=timezone.now() - timedelta(days=7)).annotate(
            view_count=Count('views')).order_by('-view_count')[:5]
        month_popular_posts = posts.filter(created_time__gte=timezone.now() - timedelta(days=30)).annotate(
            view_count=Count('views')).order_by('-view_count')[:5]

        if search_post:
            latest_posts = posts.filter(Q(tags__name=search_post))
            return render(request, 'post/post_list.html',{'latest_posts':latest_posts})
        else:
            return render(request, 'post/post_list.html', {
                'search_post': search_post,
                'latest_posts': latest_posts,
                'most_viewed_posts': most_viewed_posts,
                'week_popular_posts': week_popular_posts,
                'month_popular_posts': month_popular_posts,
                })


class PostDetailView(View):
    def get(self, request, id):
        post = Post.objects.get(id=id)
        comments = post.comments.all()
        comment_form = CommentForm()

        return render(request, 'post/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form })

    def post(self, request, id):
        post = Post.objects.get(id=id)
        comments = post.comments.all()
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.post =post
            new_comment.save()
            return render(request, 'post/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form })


class PostCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        return render(request, 'post/post_create.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()
            return redirect('post:post-list')

        return render(request, 'post/post_create.html', {'form': form})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post/post_create.html'
    form_class = PostForm


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post:post-list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)