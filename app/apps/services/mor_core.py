import logging
from urllib.parse import urlparse

import requests
from apps.services.main import BaseService
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

logger = logging.getLogger(__name__)


class MeldingenService(BaseService):
    _v = "v1"
    _api_path: str = f"/api/{_v}"
    _headers = None

    def _relatieve_url(self, url: str):
        if not isinstance(url, str):
            raise MeldingenService.BasisUrlFout("Url kan niet None zijn")
        url_o = urlparse(url)
        if not url_o.scheme and not url_o.netloc:
            return url
        if f"{url_o.scheme}://{url_o.netloc}" == self._api_base_url:
            return f"{url_o.path}{url_o.query}"
        raise MeldingenService.BasisUrlFout(
            f"url: {url}, basis_url: {self._api_base_url}"
        )

    def _get_url(self, url):
        url_o = urlparse(url)
        if not url_o.scheme and not url_o.netloc:
            return f"{self._api_base_url}{url}"
        if f"{url_o.scheme}://{url_o.netloc}" == self._api_base_url:
            return url
        raise MeldingenService.BasisUrlFout(
            f"url: {url}, basis_url: {self._api_base_url}"
        )

    def haal_token(self):
        meldingen_token = cache.get("meldingen_token")
        logger.info(f"meldingen_token exists: {bool(meldingen_token)}")
        if not meldingen_token:
            logger.info(
                f"MELDINGEN_PASSWORD EXISTS: {(settings.MELDINGEN_PASSWORD is not None)}"
            )
            email = settings.MELDINGEN_USERNAME
            try:
                validate_email(email)
            except ValidationError:
                email = f"{settings.MELDINGEN_USERNAME}@forzamor.nl"
            token_response = requests.post(
                settings.MELDINGEN_TOKEN_API,
                json={
                    "username": email,
                    "password": settings.MELDINGEN_PASSWORD,
                },
            )
            logger.info(settings.MELDINGEN_TOKEN_API)
            logger.info(settings.MELDINGEN_USERNAME)
            if token_response.status_code == 200:
                meldingen_token = token_response.json().get("token")
                cache.set(
                    "meldingen_token", meldingen_token, settings.MELDINGEN_TOKEN_TIMEOUT
                )
            else:
                raise MeldingenService.DataOphalenFout(
                    f"status code: {token_response.status_code}, response text: {token_response.text}"
                )

        return meldingen_token

    def _get_headers(self):
        if self._headers:
            return self._headers
        headers = {"Authorization": f"Token {self.haal_token()}"}
        return headers

    def __init__(self, *args, **kwargs: dict):
        self._api_base_url = settings.MELDINGEN_API_URL
        self._headers = kwargs.pop("headers", None)
        print(self._headers)
        super().__init__(*args, **kwargs)

    def aanmaken_melding(self, data):
        response = self._do_request(
            "/signaal/",
            method="post",
            data=data,
        )
        logentry = f"morcore signaal_aanmaken error: status code: {response.status_code}, text: {response.text}"
        logger.error(logentry)
        return response
