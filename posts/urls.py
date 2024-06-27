from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post),  # URL for creating a post
    path('list/', views.list_posts),  # URL for listing all posts
    path('<int:post_id>/find', views.retrieve_post),  # URL for retrieving a post
    path('<int:post_id>/update/', views.update_post),  # URL for updating a post
    path('<int:post_id>/delete/', views.delete_post),  # URL for deleting a post
    path('<int:post_id>/findCandidate/', views.findCandidate),  # URL for deleting a post

]
