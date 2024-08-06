from django.urls import path

from users.views import login_user, logout_user, register_user, settings

# from users.components.login import LoginView, logout_user
# from users.components.register import RegisterView
# from users.components.settings import SettingsView


appname = "auth"

urlpatterns = [
    path("login/", login_user, name="login"),
    path("register/", register_user, name="register"),
    path("logout/", logout_user, name="logout_user"),
    path("user/settings/", settings, name="user_settings"),
]
