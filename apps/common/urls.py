from django.urls import path
from . import views

urlpatterns = [
    path("", views.LandingPageTemplateView.as_view(), name="landing-page"),
    path("dashboard/", views.DashboardTemplateView.as_view(), name="dashboard-page"),
]
