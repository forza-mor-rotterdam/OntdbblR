import logging

from apps.main.forms import RegelChangeForm, RegelCreateForm
from apps.main.models import Regel
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

logger = logging.getLogger(__name__)


def http_404(request):
    return render(
        request,
        "404.html",
    )


def http_500(request):
    return render(
        request,
        "500.html",
    )


def root(request):
    if request.user.has_perms(["authorisatie.beheer_bekijken"]):
        return redirect(reverse("beheer"))
    return render(
        request,
        "home.html",
        {},
    )


@login_required
def ui_settings_handler(request):
    profiel = request.user.profiel
    if request.POST:
        profiel.ui_instellingen.update(
            {"fontsize": request.POST.get("fontsize", "fz-medium")}
        )
        profiel.save()

    return render(
        request,
        "snippets/form_pageheader.html",
        {"profile": profiel},
    )


@user_passes_test(lambda u: u.is_superuser)
def clear_melding_token_from_cache(request):
    cache.delete("meldingen_token")
    return HttpResponse("melding_token removed from cache")


class RegelView(View):
    model = Regel
    success_url = reverse_lazy("regel_lijst")


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.regel_lijst_bekijken", raise_exception=True),
    name="dispatch",
)
class RegelLijstView(RegelView, ListView):
    ...


class RegelCreateChangeView(RegelView):
    ...


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.regel_aanpassen", raise_exception=True),
    name="dispatch",
)
class RegelChangeView(RegelCreateChangeView, UpdateView):
    form_class = RegelChangeForm


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.regel_aanmaken", raise_exception=True),
    name="dispatch",
)
class RegelCreateView(RegelCreateChangeView, CreateView):
    form_class = RegelCreateForm


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("authorisatie.regel_verwijderen", raise_exception=True),
    name="dispatch",
)
class RegelDeleteView(RegelView, DeleteView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        return self.form_valid(form)
