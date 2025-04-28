from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('skills/', views.skills, name='skills'),
    path('projects/', views.projects, name='projects'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:post_id>/', views.post_detail, name='post_detail'),
    path('contact/', views.contact, name='contact'),
]
