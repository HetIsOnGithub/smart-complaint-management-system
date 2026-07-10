from django.urls import path

from . import views

urlpatterns = [
    path(
        "register/",
        views.register_view,
        name="register",
    ),
    path(
        "login/",
        views.login_view,
        name="login",
    ),
    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),
    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),
    path(
        "complaint/new/",
        views.submit_complaint,
        name="submit_complaint",
    ),
    path(
        "complaint/<int:pk>/",
        views.complaint_detail,
        name="complaint_detail",
    ),
    path(
        "complaint/<int:pk>/comment/",
        views.add_comment,
        name="add_comment",
    ),
    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard",
    ),
    path(
        "complaint/<int:pk>/status/",
        views.update_status,
        name="update_status",
    ),
    path(
        "complaint/<int:pk>/delete/",
        views.delete_complaint,
        name="delete_complaint",
    ),
]