from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_recruiter),
    path('list/', views.list_recruiters),
    path('<int:recruiter_id>/find/', views.retrieve_recruiter),
    path('<int:recruiter_id>/update/', views.update_recruiter),
    path('<int:recruiter_id>/delete/', views.delete_recruiter),
    path('<int:recruiter_id>/candidates_applied_to_RHposts/', views.candidates_applied_to_RHposts),
    path('<int:recruiter_id>/candidates_by_gender_per_recruiter/', views.candidates_by_gender_per_recruiter),
    path('<int:recruiter_id>/total_application_and_post/', views.total_application_and_post),

]
