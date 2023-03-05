from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('profile/<str:pk>/', views.user_profile, name="profile"),
    path('register/', views.register_user, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path(route="", view=views.home, name="home"),
    path("room/<str:pk>/", views.room, name="room"),
    path("create-room", views.create_room, name="create-room"),
    path("update-room/<str:pk>/", views.update_room, name="update-room"),
    path("delete-room/<str:pk>/", views.delete_room, name="delete-room"),
    path("delete-message/<str:pk>/", views.delete_message, name="delete-message"),
]
