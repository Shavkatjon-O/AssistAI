from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class LandingPageTemplateView(generic.TemplateView):
    template_name = "common/landing-page.html"


class DashboardTemplateView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy("account_login")

    template_name = "common/dashboard-page.html"
