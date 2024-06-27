# from .views import create_interns_from_json
from django.urls import path
from . import views


urlpatterns = [
    # path('read-and-store-data/', create_interns_from_json, name='create_interns_from_json'),
    path('internship/', views.list_Internship),
    path('internship/create/', views.create_Internship),
    path('internship/<int:internship_id>/', views.retrieve_Internship),
    path('internship/<int:internship_id>/update/', views.update_Internship),
    path('internship/<int:internship_id>/delete/', views.delete_Internship),
    path('intern/', views.list_Intern),
    path('intern/create/', views.create_Intern),
    path('intern/<int:intern_id>/', views.retrieve_Intern),
    path('intern/<int:intern_id>/update/', views.retrieve_Intern),
    path('intern/<int:intern_id>/delete/', views.retrieve_Intern),
    path('start_scraping/<int:Internship_id>/', views.start_scraping),
    path('all_Internship_Interns/<int:Internship_id>/', views.all_Internship_Interns),
    path('code_outlook/<int:Internship_id>/', views.code_outlook, name='code_outlook'),
    

]