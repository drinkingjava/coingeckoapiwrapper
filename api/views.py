import json
from datetime import datetime

import requests
from requests.exceptions import HTTPError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

API_URL_BASE = 'https://api.coingecko.com/api/v3/'


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List': '/coinList',
        'Detail': '/marketCap'
    }
    return Response(api_urls)


@api_view(['GET'])
def coin_list(request):
    try:
        url = f'{API_URL_BASE}coins/list'
        response = requests.get(url)
        response.raise_for_status()
        return Response(json.loads(response.text))
    except HTTPError as err:
        return Response(f'{err}', status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def market_cap(request):
    params = request.query_params.copy()
    err_msg = {
        'detail': 'id, date and currency are required query params e.g '
                  '/marketCap?id=chainlink&date=30/12/2017&currency=gbp'
    }
    try:
        id = params.pop('id')[0]
        cur = params.pop('currency')[0]
        gecko_date = _convert_date(params.pop('date')[0])
        url = f'{API_URL_BASE}coins/{id}/history?date={gecko_date}'
        ''' In case of extra supported parameters '''
        if params:
            for k, v in params.items():
                url += f'&{k}={v}'

        response = requests.get(url)
        response.raise_for_status()
        price = {}
        price[cur] = (json.loads(response.text)
                      ['market_data']['market_cap'][cur])
        return Response(price)
    except KeyError as key:
        err_msg['error'] = f'{key} not provided'
        return Response(err_msg, status=status.HTTP_400_BAD_REQUEST)
    except HTTPError as err:
        err_msg['error'] = f'{err}'
        return Response(err_msg, status=status.HTTP_404_NOT_FOUND)


def _convert_date(datestring):
    format_string = '%d/%m/%Y'
    date_object = datetime.strptime(datestring, format_string)
    return date_object.strftime('%d-%m-%Y')
