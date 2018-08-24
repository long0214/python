from django.urls import path, re_path
from . import views


urlpatterns = [
        path('get/<str:query>/', views.get),
        path('add/', views.add),
        path('delete/', views.delete)
]
