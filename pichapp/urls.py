from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('create_room/', views.create_room, name='create_room'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('rooms/<int:pk>/participants/join', views.join_room, name='room_join'),
    path('rooms/<int:pk>/participants/exit', views.exit_room, name='room_exit'),
    path('search_room/', views.search_room, name='search_room'),
    path('', views.home_view, name='home_view')
]
