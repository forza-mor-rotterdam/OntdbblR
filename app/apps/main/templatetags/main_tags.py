import json
import os
from datetime import datetime

from apps.main.services import render_onderwerp as render_onderwerp_service
from django import template
from django.conf import settings

register = template.Library()


@register.filter
def replace_comma_by_dot(value):
    return str(value).replace(",", ".")


@register.filter
def to_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")
    except Exception as e:
        print(e)
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
    except Exception as e:
        print(e)
    return value


@register.filter
def to_timestamp(value):
    try:
        return int(value.timestamp())
    except Exception:
        print("No datatime instance")


@register.filter
def json_encode(value):
    return json.dumps(value)


@register.simple_tag
def vind_in_dict(op_zoek_dict, key):
    if not isinstance(op_zoek_dict, dict):
        return key
    result = op_zoek_dict.get(key, op_zoek_dict.get(str(key), key))
    if isinstance(result, (list, tuple)):
        return result[0]
    return result


@register.filter
def adres_order_nummer(taak, taken_sorted):
    return taken_sorted.get(taak.id, taak.id)


@register.filter
def mor_core_url(initial_url):
    return f"{settings.MOR_CORE_URL_PREFIX}{initial_url}"


@register.simple_tag
def render_onderwerp(onderwerp_url):
    return render_onderwerp_service(onderwerp_url)


@register.filter
def file_exists(file_path):
    return os.path.isfile(
        os.path.join(settings.BASE_DIR, "apps/main/templates/", file_path)
    )
