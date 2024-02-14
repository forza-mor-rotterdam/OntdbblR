import logging

from apps.services.basis import BasisService
from django.conf import settings
from django.template.loader import get_template
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)


def render_onderwerp(onderwerp_url, standaar_naam=None):
    groepen = OnderwerpenService().get_groepen_lijst().get("results", [])
    groepnaam_door_uuid = {g.get("uuid"): g.get("name") for g in groepen}
    onderwerp = OnderwerpenService().get_onderwerp(onderwerp_url)
    standaard_naam = f"{groepnaam_door_uuid.get(onderwerp.get('group_uuid'), onderwerp.get('group_uuid'))} - {onderwerp.get('name', 'Niet gevonden!' if not standaar_naam else standaar_naam)}"
    if onderwerp.get("priority") == "high":
        spoed_badge = get_template("badges/spoed.html")
        return mark_safe(f"{standaard_naam}{spoed_badge.render()}")
    return standaard_naam


class OnderwerpenService(BasisService):
    def get_onderwerp(self, url) -> dict:
        return self.do_request(url, cache_timeout=60 * 10, raw_response=False)

    def get_groepen_lijst(self) -> dict:
        if not settings.ONDERWERPEN_URL:
            logger.warning("Env var 'ONDERWERPEN_URL' is niet gezet")
            return {"count": 0, "results": []}
        url = f"{settings.ONDERWERPEN_URL}/api/v1/group"
        return self.do_request(
            url,
            cache_timeout=60 * 10,
            raw_response=False,
            params={
                "limit": 1000,
            },
        )

    def get_onderwerpen_lijst(self) -> dict:
        if not settings.ONDERWERPEN_URL:
            logger.warning("Env var 'ONDERWERPEN_URL' is niet gezet")
            return {"count": 0, "results": []}
        url = f"{settings.ONDERWERPEN_URL}/api/v1/category"
        return self.do_request(
            url,
            cache_timeout=60 * 10,
            raw_response=False,
            params={
                "limit": 1000,
            },
        )
