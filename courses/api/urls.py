from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('subjects/', views.SubjectListView, name='subject_list'),
    path('subjects/<pk>', views.SubjectDetailView, name='subject_detail'),
]
