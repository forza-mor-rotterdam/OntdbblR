
from rest_framework import serializers
import base64
import binascii
from django.core.exceptions import ValidationError


class Base64Field(serializers.CharField):
    EMPTY_VALUES = [None, "", [], (), {}]
    def to_internal_value(self, base64_data):
        # Check if this is a base64 string
        if base64_data in self.EMPTY_VALUES:
            return None

        if isinstance(base64_data, str):

            # Try to decode the file. Return validation error if it fails.
            try:
                base64.b64decode(base64_data)
            except (TypeError, binascii.Error, ValueError):
                raise ValidationError("String can not be decode to a file")

            return super().to_internal_value(base64_data)

        raise ValidationError(f"Invalid type. This is not an base64 string: {type(base64_data)}")


class BijlageSerializer(serializers.Serializer):
    """
    Bijlage serializer
    """

    bestand = Base64Field()