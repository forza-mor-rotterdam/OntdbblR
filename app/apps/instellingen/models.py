from django.contrib.gis.db import models
from utils.models import BasisModel


class Instelling(BasisModel):
    mor_core_basis_url = models.URLField(default="http://core.mor.local:8002")
    onderwerpen_basis_url = models.URLField(default="http://onderwerpen.mor.local:8006")

    @classmethod
    def actieve_instelling(cls):
        actieve_instellingen = cls.objects.all()
        if not actieve_instellingen:
            raise Exception("Er zijn nog geen instellingen aangemaakt")
        return actieve_instellingen[0]

    def valideer_url(self, veld, url):
        if veld not in (
            "mor_core_basis_url",
            "onderwerpen_basis_url",
        ):
            return False
        return url.startswith(getattr(self, veld))
