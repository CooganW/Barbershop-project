from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from bookings.views import home, appointment_view

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("appointment/", appointment_view, name="appointment"),
    path("api/", include("bookings.urls")),
    path("api/auth/", include("userauth.urls")),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.logout_then_login, name="logout"),
]
