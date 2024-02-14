from rest_framework import serializers
from rest_framework_gis.fields import GeometryField


class AdresSerializer(serializers.Serializer):
    plaatsnaam = serializers.CharField(
        max_length=255, required=False, allow_blank=True, allow_null=True
    )
    straatnaam = serializers.CharField(
        max_length=255, required=False, allow_blank=True, allow_null=True
    )
    huisnummer = serializers.IntegerField(required=False)
    huisletter = serializers.CharField(
        max_length=1, required=False, allow_blank=True, allow_null=True
    )
    toevoeging = serializers.CharField(
        max_length=4, required=False, allow_blank=True, allow_null=True
    )
    postcode = serializers.CharField(
        max_length=7, required=False, allow_blank=True, allow_null=True
    )
    buurtnaam = serializers.CharField(
        max_length=255, required=False, allow_blank=True, allow_null=True
    )
    wijknaam = serializers.CharField(
        max_length=255, required=False, allow_blank=True, allow_null=True
    )
    geometrie = GeometryField(required=False)


class GrafSerializer(serializers.Serializer):
    plaatsnaam = serializers.CharField(max_length=255)
    begraafplaats = serializers.CharField(max_length=50)
    grafnummer = serializers.CharField(
        max_length=10, required=False, allow_blank=True, allow_null=True
    )
    vak = serializers.CharField(
        max_length=10, required=False, allow_blank=True, allow_null=True
    )
    geometrie = GeometryField(required=False)


class LichtmastSerializer(serializers.Serializer):
    lichtmast_id = serializers.CharField(max_length=255)
    geometrie = GeometryField(required=False)


class GeometrieSerializer(serializers.Serializer):
    geometrie = GeometryField(required=False)
