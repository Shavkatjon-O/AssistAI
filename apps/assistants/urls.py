from django.urls import path
from . import views

urlpatterns = [
    path(
        "assistants-list/", views.AssistantsListView.as_view(), name="assistants-list"
    ),
]
