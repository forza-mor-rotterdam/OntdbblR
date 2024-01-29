import logging

from apps.services.mor_core import MeldingenService
from apps.signalen.serializers import SignaalSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class SignaalViewSet(viewsets.ViewSet):
    serializer_class = SignaalSerializer

    http_method_names = ["post"]

    permission_classes = ()

    def create(self, request):
        serializer = SignaalSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            auth_header = (
                {"Authorization": request.headers.get("Authorization")}
                if request.headers.get("Authorization")
                else None
            )
            response = MeldingenService(headers=auth_header).aanmaken_melding(
                serializer.data
            )
            logger.info(
                f"Response van splitter: text={response.text}, status={response.status_code}"
            )
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
