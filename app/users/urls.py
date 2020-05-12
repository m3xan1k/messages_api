from django.urls import path

from users import views

urlpatterns = [
    path('users/', views.UsersView.as_view(), name=views.UsersView.name),
    path('users/<str:id>/', views.UserView.as_view(), name=views.UserView.name),
]
