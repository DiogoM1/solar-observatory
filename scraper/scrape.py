#!/usr/bin/env python -f

import os
import time
import requests
from prometheus_client import start_http_server, Gauge


host = os.getenv('ENVOY_HOST')

production_gauges = {
    'activeCount': Gauge('production_active_count', 'Active Count', ['type']),
    'wNow': Gauge('power_now_watts', 'Active Count', ['type']),
    'whToday': Gauge('production_today_watthours', 'Total production today', ['type']),
    'whLastSevenDays': Gauge('production_7days_watthours', 'Total production last seven days', ['type']),
    'whLifetime': Gauge('production_lifetime_watthours', 'Total production lifetime', ['type']),
}

consumption_gauges = {
    'wNow': Gauge('consumption_now_watts', 'Active Count', ['type']),
    'whToday': Gauge('consumption_today_watthours', 'Total consumption today', ['type']),
    'whLastSevenDays': Gauge('consumption_7days_watthours', 'Total consumption last seven days', ['type']),
    'whLifetime': Gauge('consumption_lifetime_watthours', 'Total consumption lifetime', ['type']),
}


def scrape_production_json():
    url = 'http://%s/production.json' % host
    data = requests.get(url).json()
    production = data['production']
    print(production)
    for each in production:
        mtype = each['type']
        for key in ['activeCount', 'wNow', 'whLifetime', 'whToday', 'whLastSevenDays']:
            value = each.get(key)
            if value is not None:
                production_gauges[key].labels(type=mtype).set(value)
    consumption = data['consumption']
    print(consumption)
    for each in consumption:
        mtype = each['measurementType']
        for key in ['wNow', 'whLifetime', 'whToday', 'whLastSevenDays']:
            value = each.get(key)
            if value is not None:
                consumption_gauges[key].labels(type=mtype).set(value)

def main():
    start_http_server(8000)
    while True:
        try:
            scrape_production_json()
        except Exception as e:
            print('Exception fetching scrape data: %s' % e)
        time.sleep(60)


if __name__ == '__main__':
    main()
