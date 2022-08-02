from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import NewsForm, ArticleForm
from .filters import PostFilter


class PostList(ListView):
    model = Post
    ordering = '-date_and_time_of_creation_post'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


class PostDetail(DetailView):
    model = Post
    template_name = 'single_news.html'
    context_object_name = 'single_news'


class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW'
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'


class ArticleUpdate(UpdateView):
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')


# class SearchNews(ListView):
#     model = Post
#     template_name = 'search_news.html'
#     context_object_name = 'search_news'
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['time_now'] = datetime.utcnow()
#         context['filterset'] = self.filterset
#         return context
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         self.filterset = PostFilter(self.request.GET, queryset)
#         return self.filterset.qs
