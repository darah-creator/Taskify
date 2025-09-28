from django.urls import path
from . import views

urlpatterns = [
    # User
    path("<int:pk>/submit/", views.submit_task, name="submit_task"),

    # Admin
    path("create/", views.create_task, name="create_task"),
    path("<int:pk>/review/", views.review_task, name="review_task"),
    path("<int:pk>/delete_task/", views.delete_task, name="delete_task"),

]
