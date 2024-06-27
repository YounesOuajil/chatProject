    
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_candidate),  # URL for creating a candidate
    path('list/', views.list_candidates),  # URL for listing all candidate
    path('<int:candidate_id>/find', views.retrieve_candidate),  # URL for retrieving a candidate
    path('<int:candidate_id>/update/', views.update_candidate),  # URL for updating a candidate
    path('<int:candidate_id>/delete/', views.delete_candidate),  # URL for deleting a candidate
    path('apply_for_job/', views.apply_for_job), 
    # path('<int:candidate_id>/<int:post_id>/apply_for_job/', views.apply_for_job), 

    
]