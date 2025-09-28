from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    # /dashboard/ -> route to appropriate dashboard based on role
    path("", views.dashboard_home, name="home"),

    # /dashboard/user/  (explicit user dashboard)
    path("user/", views.user_dashboard, name="user_dashboard"),

    # /dashboard/admin/ (admin-only)
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
]
