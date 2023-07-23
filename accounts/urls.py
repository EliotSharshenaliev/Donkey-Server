from django.urls import path

from accounts import views

urlpatterns = [
    path("signup", views.SignUpView.as_view(), name="signup"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogOutView.as_view(), name="logout"),
    path("get-user", views.GetUser.as_view(), name="logout"),

    path("register_users/", views.RegisterBoxListCreateAPIView.as_view(), name="register user list")

]
