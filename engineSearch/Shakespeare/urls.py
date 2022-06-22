from django.urls import path

from . import views

app_name = 'Shakespeare'
urlpatterns = [
    # ex: /searchShakespeare/
    path('', views.index, name='index'),
    # ex: /searchShakespeare/5/
    path('<int:pk>/content/', views.detail, name='detail'),
    # ex: /searchShakespeare/result/
    path('results/', views.results, name='results'),
]