from django.conf import settings
from charts.models import Charts
from celery import shared_task
from utils import TypeMetal
import requests


@shared_task
def live_price():
    try:
        resp = requests.get(settings.LIVE_PRICE_URL)
        if resp.status_code != 200:
            return

        data = resp.json()[0]

        # save sliver price
        Charts.create_charts(**{
            "type": TypeMetal.SILVER,
            "world_sell_price": 0,
            "world_buy_price": 0,
            "local_sell_price": data['Sell_silver'],
            "local_buy_price": data['Buy_silver']
        })

        # save gold price
        Charts.create_charts(**{
            "type": TypeMetal.GOLD,
            "world_sell_price": data['WorldPriceSell'],
            "world_buy_price": data['WorldPrice'],
            "local_sell_price": data['Sell'],
            "local_buy_price": data['Buy']
        })

    except (requests.RequestException,
            requests.JSONDecodeError,
            requests.ConnectTimeout,
            requests.ReadTimeout) as e:

        return
