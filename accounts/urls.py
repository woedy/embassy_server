from django.urls import path, include, re_path

from accounts.views import RegisterView, LoginView, logout_view, AccountEmailActivateView, login_view

app_name = "accounts"

urlpatterns = [
    #path("login/", LoginView.as_view(), name="login"),
    path("login/", login_view, name="login"),

    path("logout/", logout_view, name="logout"),

    path("register/", RegisterView.as_view(), name="register"),

re_path(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$',
            AccountEmailActivateView.as_view(),
            name='email-activate'),
    re_path(r'^email/resend-activation/$',
            AccountEmailActivateView.as_view(),
            name='resend-activation'),


]
