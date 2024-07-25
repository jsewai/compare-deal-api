from django.urls import path

from bookmark import views

app_name = 'bookmark'

urlpatterns = [
    path('', views.ListBookmarkView.as_view(), name='list_bookmark'),
    path('add/', views.ListCreateBookmarkView.as_view(), name='create_bookmark'),
    path('delete/<int:pk>/', views.DestroyBookmarkView.as_view(), name='delete_bookmark'),
]