from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.SnippedDetailView.as_view(), name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('snippets/<str:slug>/',
         views.LanguageSnippetView.as_view(), name='language'),
    path('snippets/user/<str:username>/',
         views.UserSnippetView.as_view(), name='user_snippets'),
    path('snippets/ver/<int:pk>',
         views.UserSnippedDetailView.as_view(), name='snippet'),
    path('snippets/', views.CreateSnippedView.as_view(), name='snippets'),
    path('snippets/edit/<int:pk>',
         views.SnippetUpdateView.as_view(), name='snippet_edit'),
]
