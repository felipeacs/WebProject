from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', views.ChartData.as_view()),
    path('covid/', views.home, name='home'),
]

