import copy
import json
import logging
from datetime import datetime, timedelta

from apps.main.models import Regel
from apps.main.services import MORCoreService
from apps.signalen.serializers import SignaalSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response

logger = logging.getLogger(__name__)


def stringdatetime_naar_datetime(text):
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            ...
    raise ValueError("no valid date format found")


class SignaalViewSet(viewsets.ViewSet):
    serializer_class = SignaalSerializer

    http_method_names = ["post"]

    permission_classes = ()

    def create(self, request):
        serializer = SignaalSerializer(data=request.data)
        token = [
            auth_part.strip()
            for auth_part in request.headers.get("Authorization", "").split(" ")
        ][-1]
        mor_core_service = MORCoreService(token=token)
        is_valid = serializer.is_valid(raise_exception=True)
        if is_valid:
            signaal_data = copy.deepcopy(serializer.data)
            logger.info(f"Request splitter data: {json.dumps(signaal_data, indent=4)}")

            regel = Regel.objects.filter(
                onderwerp_url__in=[
                    o.get("bron_url") for o in signaal_data.get("onderwerpen")
                ]
            ).first()
            adressen = signaal_data.get("adressen")
            coordinates = (
                adressen[0].get("geometrie", {}).get("coordinates", [])
                if adressen
                else None
            )
            origineel_aangemaakt = stringdatetime_naar_datetime(
                signaal_data.get("origineel_aangemaakt")
            )
            logger.info(
                f"Signaal: origineel_aangemaakt={signaal_data.get('origineel_aangemaakt')}, coords={coordinates}"
            )
            if regel and regel.deduplicate and coordinates:
                logger.info("ONTDUBBEL")
                # check bij mor-core of er meldingen aan deze regel voldoen
                params = {
                    "onderwerp_url": regel.onderwerp_url,
                    "within": f"lon:{coordinates[0]},lat:{coordinates[1]},d:{regel.distance}",
                    "origineel_aangemaakt_gt": (
                        origineel_aangemaakt - timedelta(seconds=regel.max_age)
                    ).isoformat(),
                    "status": [
                        "openstaand",
                        "in_behandeling",
                        "controle",
                        "wachten_melder",
                        "pauze",
                    ],
                    "ordering": "origineel_aangemaakt",
                    "limit": "5",
                }
                meldingen_data = mor_core_service.get_meldingen(params)
                logger.info("Melding check voor dubbele meldingen")

                if meldingen_data.get("errors"):
                    logger.error(
                        f'Meldingen response: error={meldingen_data.get("errors")}'
                    )
                try:
                    logger.info(
                        f"Melding check voor dubbele meldingen: count={meldingen_data.get('count')}, first 5 below"
                    )
                    for m in meldingen_data.get("results", [])[:5]:
                        logger.info(
                            f"M: id={m.get('id')}, origineel_aangemaakt={m.get('origineel_aangemaakt')}, coords: {m.get('locaties_voor_melding', [])[0].get('geometrie', {}).get('coordinates', []) if m.get('locaties_voor_melding') and m.get('locaties_voor_melding', [])[0].get('geometrie') else []}"
                        )
                    if meldingen_data.get("count") > 0:
                        logger.info(
                            f"Melding check voor dubbele meldingen: eerste melding={json.dumps(meldingen_data.get('results')[0], indent=4)}"
                        )
                        signaal_data["melding"] = meldingen_data.get("results")[0].get(
                            "id"
                        )
                except Exception as e:
                    logger.error(f"meldingen inspect fout={e}")

            logger.info(f"Signaal aanmaken data: {json.dumps(signaal_data, indent=4)}")

            response = mor_core_service.signaal_aanmaken(data=signaal_data)

            status_code = (
                response.get("error", {}).get("status_code")
                if response.get("error", {})
                else 201
            )
            logger.info(
                f"signaal_aanmaken response van mor-core: text={response}, status={status_code}"
            )
            return Response(response, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
