from django.urls import path

from search import views

app_name = 'search'

urlpatterns = [
    path('kijiji/', views.kijiji, name='kijiji'),
    path('google/', views.google, name='google'),
]