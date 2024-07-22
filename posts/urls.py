

from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('important/', views.important_view, name='important'),
    path('add_todo/', views.add_todo, name='add_todo'),
    path('important_add_todo/', views.important_add_todo, name='important_add_todo'),
    path('priority_update/<int:post_id>/', views.priority_update, name='priority_update'),
    path('completed_update/<int:post_id>/', views.completed_update, name='completed_update'),
    path('post/<int:post_id>/', views.post_details, name='post-details'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/update/', views.post_update, name='post_update'),
    path('search/', views.search, name='search'),
    path('search/<str:query>/', views.search, name='search_with_query'),
    path('important_search/', views.important_search, name='important_search'),
    path('important_search/<str:query>/', views.important_search, name='important_search_with_query'),
]
