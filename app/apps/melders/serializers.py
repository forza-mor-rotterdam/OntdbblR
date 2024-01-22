from rest_framework import serializers


class MelderSerializer(serializers.Serializer):
    naam = serializers.CharField(max_length=100, allow_blank=True, required=False)
    voornaam = serializers.CharField(max_length=50, allow_blank=True, required=False)
    achternaam = serializers.CharField(max_length=50, allow_blank=True, required=False)
    email = serializers.EmailField(allow_blank=True, required=False)
    telefoonnummer = serializers.CharField(max_length=17, allow_blank=True, required=False)
