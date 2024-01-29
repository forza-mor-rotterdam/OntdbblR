from apps.bijlagen.serializers import BijlageSerializer
from apps.locatie.serializers import (
    AdresSerializer,
    GrafSerializer,
    LichtmastSerializer,
)
from apps.melders.serializers import MelderSerializer
from rest_framework import serializers


class OnderwerpSerializer(serializers.Serializer):
    bron_url = serializers.URLField()


class SignaalSerializer(serializers.Serializer):
    signaal_url = serializers.URLField()
    bijlagen = BijlageSerializer(many=True, required=False)
    melder = MelderSerializer(required=False)

    melding = serializers.IntegerField(required=False)
    bron_id = serializers.CharField(max_length=500)
    bron_signaal_id = serializers.CharField(max_length=500)
    omschrijving_kort = serializers.CharField(max_length=500)
    omschrijving = serializers.CharField(
        max_length=5000, allow_blank=True, required=False
    )
    meta = serializers.JSONField(default=dict)
    meta_uitgebreid = serializers.JSONField(default=dict)
    adressen = AdresSerializer(many=True, required=False)
    lichtmasten = LichtmastSerializer(many=True, required=False)
    graven = GrafSerializer(many=True, required=False)
    origineel_aangemaakt = serializers.DateTimeField()
    onderwerpen = serializers.ListSerializer(child=OnderwerpSerializer())
