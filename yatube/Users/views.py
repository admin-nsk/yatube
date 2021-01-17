from django.views.generic import CreateView

from django.urls import reverse_lazy
from .form import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"