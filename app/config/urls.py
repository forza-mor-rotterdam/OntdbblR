from apps.authenticatie.views import (
    GebruikerAanmakenView,
    GebruikerAanpassenView,
    GebruikerLijstView,
    LoginView,
    LogoutView,
    gebruiker_bulk_import,
)
from apps.authorisatie.views import (
    RechtengroepAanmakenView,
    RechtengroepAanpassenView,
    RechtengroepLijstView,
    RechtengroepVerwijderenView,
)
from apps.beheer.views import beheer
from apps.main.views import (
    RegelChangeView,
    RegelCreateView,
    RegelDeleteView,
    RegelLijstView,
    clear_melding_token_from_cache,
    http_404,
    http_500,
    root,
    ui_settings_handler,
)
from apps.signalen.viewsets import SignaalViewSet
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"signaal", SignaalViewSet, basename="signaal")

urlpatterns = [
    path("", root, name="root"),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path("api/v1/", include((router.urls, "app"), namespace="v1")),
    path("api-token-auth/", views.obtain_auth_token),
    path("part/pageheader-form/", ui_settings_handler, name="pageheader_form_part"),
    path(
        "admin/clear-melding-token-from-cache/",
        clear_melding_token_from_cache,
        name="clear_melding_token_from_cache",
    ),
    path("admin/", admin.site.urls),
    path("oidc/", include("mozilla_django_oidc.urls")),
    path("health/", include("health_check.urls")),
    # START beheer
    path("beheer/", beheer, name="beheer"),
    path("beheer/gebruiker/", GebruikerLijstView.as_view(), name="gebruiker_lijst"),
    path(
        "beheer/gebruiker/bulk-import/",
        gebruiker_bulk_import,
        name="gebruiker_bulk_import",
    ),
    path(
        "beheer/gebruiker/aanmaken/",
        GebruikerAanmakenView.as_view(),
        name="gebruiker_aanmaken",
    ),
    path(
        "beheer/gebruiker/<int:pk>/aanpassen/",
        GebruikerAanpassenView.as_view(),
        name="gebruiker_aanpassen",
    ),
    path(
        "beheer/rechtengroep/",
        RechtengroepLijstView.as_view(),
        name="rechtengroep_lijst",
    ),
    path(
        "beheer/rechtengroep/aanmaken/",
        RechtengroepAanmakenView.as_view(),
        name="rechtengroep_aanmaken",
    ),
    path(
        "beheer/rechtengroep/<int:pk>/aanpassen/",
        RechtengroepAanpassenView.as_view(),
        name="rechtengroep_aanpassen",
    ),
    path(
        "beheer/rechtengroep/<int:pk>/verwijderen/",
        RechtengroepVerwijderenView.as_view(),
        name="rechtengroep_verwijderen",
    ),
    path("beheer/regel/", RegelLijstView.as_view(), name="regel_lijst"),
    path(
        "beheer/regel/aanmaken/",
        RegelCreateView.as_view(),
        name="regel_aanmaken",
    ),
    path(
        "beheer/regel/<int:pk>/aanpassen/",
        RegelChangeView.as_view(),
        name="regel_aanpassen",
    ),
    path(
        "beheer/regel/<int:pk>/verwijderen/",
        RegelDeleteView.as_view(),
        name="regel_verwijderen",
    ),
    # END beheer
    path("api/schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema"),
    # Optional UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

if not settings.ENABLE_DJANGO_ADMIN_LOGIN:
    urlpatterns += [
        path(
            "admin/login/",
            RedirectView.as_view(url="/login/?next=/admin/"),
            name="admin_login",
        ),
        path(
            "admin/logout/",
            RedirectView.as_view(url="/logout/?next=/"),
            name="admin_logout",
        ),
    ]

if settings.OIDC_ENABLED:
    urlpatterns += [
        path("oidc/", include("mozilla_django_oidc.urls")),
    ]

urlpatterns += [
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("404/", http_404, name="404"),
        path("500/", http_500, name="500"),
    ]
