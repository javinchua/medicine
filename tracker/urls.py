from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("morning", views.morning, name="morning"),
    path("afternoon", views.afternoon, name="afternoon"),
    path("night", views.night, name="night"),
    path("create_medicine", views.create_medicine, name="create_medicine"),
    path("take/<int:medicine_id>", views.take, name="take"),
    path("reset", views.reset, name="reset")
]