from apps.services.onderwerpen import OnderwerpenService
from django.contrib.gis.db import models
from utils.models import BasisModel


class Regel(BasisModel):
    """
    Ontdubbel regel voor meldingen
    """

    onderwerp_url = models.URLField(
        unique=True,
    )
    deduplicate = models.BooleanField(default=True)
    distance = models.PositiveIntegerField(
        default=30,
        help_text="De straal om de binnenkomende gps coordinaten in meters",
    )
    max_age = models.PositiveIntegerField(
        default=864000,
        help_text="Tijd in seconden na het begin van de melding",
    )

    def __str__(self):
        onderwerp = OnderwerpenService().get_onderwerp(self.onderwerp_url)
        if onderwerp:
            return onderwerp.get("name")
        return self.onderwerp_url
