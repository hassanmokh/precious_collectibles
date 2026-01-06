import requests
from django.conf import settings


def validate_domain_email(email):
    try:
        resp = requests.get(f"{settings.ABSTRACT_BASE_URL}email={email}")
        if resp.status_code != 200:
            return False

        if resp.json().get("deliverability", None) == 'DELIVERABLE':
            return True

    except (requests.RequestException,
            requests.JSONDecodeError,
            requests.ConnectTimeout,
            requests.ReadTimeout) as e:
        return False

    return False
