from django.urls import path

from . import views

urlpatterns = [
    path("csrf/", views.csrf_token, name="csrf"),
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("me/", views.current_user, name="current-user"),
    path("dealers/", views.dealers, name="dealers"),
    path("dealers/<int:dealer_id>/", views.dealer_detail, name="dealer-detail"),
    path("dealers/<int:dealer_id>/reviews/", views.dealer_reviews, name="dealer-reviews"),
    path("reviews/", views.create_review, name="create-review"),
    path("cars/", views.car_makes, name="car-makes"),
    path("analyze-review/", views.analyze_review, name="analyze-review"),
]
