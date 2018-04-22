from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic        import TemplateView, CreateView
from django.views.generic.edit   import DeleteView, UpdateView
from django.views.generic.list   import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Q
from functools import reduce
import operator

from .models import Post, Comment, Category
from .form import PostForm, SigninForm, CommentForm, AddCategoryForm


class HomeView(TemplateView):
    template_name = 'board/home.html'


class SigninView(CreateView):
    template_name = 'board/signin.html'
    model = User
    form_class = SigninForm
    success_url = reverse_lazy('board:index')


class BaseIndexView(ListView):
    model = Post
    template_name = 'board/index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.order_by('-date_posted')


class WordSearchIndexView(BaseIndexView):

    def get_queryset(self):
        result = super().get_queryset()
        keywords = self.request.GET.get("q")
        if keywords:
            keyword_list = keywords.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in keyword_list)) |
                reduce(operator.and_,
                       (Q(content__icontains=q) for q in keyword_list))|
                reduce(operator.and_,
                       (Q(user__icontains=q) for q in keyword_list))
            )
        return result

class CategorySearchView(BaseIndexView):

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.kwargs.get("c")
        if category:
            queryset = queryset.filter(category__name=category)

        return queryset


class ContentView(DetailView):
    model = Post
    template_name = 'board/content.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('date_posted')
        return context


class PostFormView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "board/form_new_post.html"
    success_url = reverse_lazy("board:index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.date_posted = timezone.now()
        return super().form_valid(form)


class DeletePostView(DeleteView):
    model = Post
    template_name = "board/delete_post.html"
    success_url = reverse_lazy("board:index")


class UpdatePostView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "board/update_post.html"
    success_url = '/'

    def get_success_url(self, **kwargs):
        return reverse_lazy('board:index')


class CommentFormView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "board/form.html"
    success_url = "/"

    def get_success_url(self, **kwargs):
        return reverse_lazy('board:content', kwargs={'pk': self.kwargs['pk']})


    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.date_posted = timezone.now()
        comment = form.save(commit=False)
        post_id = self.kwargs['pk']
        post = get_object_or_404(Post, id=post_id)
        comment.post = post
        return super(CommentFormView, self).form_valid(form)

class CategoryListView(ListView):
    model = Category
    template_name = 'board/category_list.html'
    context_object_name = 'categories'


class CategoryAddView(CreateView):
    model = Category
    form_class = AddCategoryForm
    template_name = 'board/category_add.html'
    success_url = reverse_lazy('board:add_post')
