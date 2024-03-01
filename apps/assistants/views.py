from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from . import models


class AssistantsListView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy("account_login")

    model = models.Assistant
    template_name = "assistants/assistants-list.html"
