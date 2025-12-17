import logging

from apps.instellingen.models import Instelling
from django.contrib import messages
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from mor_api_services import MORCoreService as BasisMORCoreService
from mor_api_services import OnderwerpenService as BasisOnderwerpenService

logger = logging.getLogger(__name__)


def standaard_fout_afhandeling(service, response=None, fout=""):
    log = (
        f"API antwoord fout: {service.naar_json(response)}, status code: {response.status_code}"
        if not fout
        else f"Generiek fout: {fout}"
    )
    logger.error(log)

    message = (
        f'Er ging iets mis!: {service.naar_json(response).get("detail", "Geen detail gevonden")}, {service.__class__.__name__}[{response.status_code}]'
        if not fout
        else f"Er ging iets mis!: {service.__class__.__name__}"
    )
    if service._request:
        messages.error(service._request, message)

    return {
        "error": log,
    }


class MORCoreService(BasisMORCoreService):
    def __init__(self, *args, **kwargs):
        instellingen = Instelling.actieve_instelling()
        kwargs.update(
            {
                "basis_url": instellingen.mor_core_basis_url,
                "client_name": "OntdbblR",
            }
        )
        super().__init__(*args, **kwargs)

    def met_fout(self, response=None, fout=""):
        return standaard_fout_afhandeling(self, response, fout)


class OnderwerpenService(BasisOnderwerpenService):
    def __init__(self, *args, **kwargs):
        instellingen = Instelling.actieve_instelling()
        kwargs.update(
            {
                "basis_url": instellingen.onderwerpen_basis_url,
                "client_name": "OntdbblR",
            }
        )
        super().__init__(*args, **kwargs)

    def met_fout(self, response=None, fout=""):
        return standaard_fout_afhandeling(self, response, fout)


def render_onderwerp(onderwerp_url, standaar_naam=None):
    onderwerpen_service = OnderwerpenService()

    groepen = onderwerpen_service.get_groepen()
    groepnaam_door_uuid = {g.get("uuid"): g.get("name") for g in groepen}
    onderwerp = onderwerpen_service.get_onderwerp(onderwerp_url)
    standaard_naam = f"{groepnaam_door_uuid.get(onderwerp.get('group_uuid'), onderwerp.get('group_uuid'))} - {onderwerp.get('name', 'Niet gevonden!' if not standaar_naam else standaar_naam)}"
    if onderwerp.get("priority") == "high":
        spoed_badge = get_template("badges/spoed.html")
        return mark_safe(f"{standaard_naam}{spoed_badge.render()}")
    return standaard_naam
