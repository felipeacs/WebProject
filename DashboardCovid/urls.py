from django.urls import path

from . import views

urlpatterns = [
    path('', views.ExecutionsView.as_view(), name='ExecutionsView'),
    path('dash/', views.dashboard, name='dashboard'),
    path('api/', views.ChartData.as_view()),
    path('covid/', views.home, name='home'),
]

