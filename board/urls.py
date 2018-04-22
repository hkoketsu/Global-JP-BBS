from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .form import LoginForm

from . import views

app_name = 'board'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('index/', views.BaseIndexView.as_view(), name='index'),
    path('index/word_search', views.WordSearchIndexView.as_view(), name='word_search'),
    url(r'^index/category=(?P<c>\w+)',views.CategorySearchView.as_view(), name='category_search'),
    path('<int:pk>/', views.ContentView.as_view(), name='content'),
    path('form/', views.PostFormView.as_view(), name='add_post'),
    path('<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('<int:pk>/update/', views.UpdatePostView.as_view(), name='update_post'),
    path('<int:pk>/comment/', views.CommentFormView.as_view(), name='comment'),


    path('login/', auth_views.login, {'template_name': 'board/login.html', 'authentication_form': LoginForm }, name='login'),
    path('logout/', auth_views.logout, {'template_name': 'board/home.html'}, name='logout'),
    path('signin/', views.SigninView.as_view(), name='signin'),

    path('index/category_list/', views.CategoryListView.as_view(), name='category_list'),
    path('index/category_list/add/', views.CategoryAddView.as_view(), name='category_add'),

]