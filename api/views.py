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
        url = f'{API_URL_BASE}/coins/list'
        response = requests.get(url)
        response.raise_for_status()
        return Response(json.loads(response.text))
    except HTTPError as err:
        return Response(f'{err}', status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def market_cap(request):
    params = request.query_params.copy()
    id = params.pop('id')[0]
    url = f'{API_URL_BASE}coins/{id}/history'

    if params:
        url += '?'
        for k, v in params.items():
            if k == 'date':
                gecko_date = _convert_date(v)
                url += f'{k}={gecko_date}&'
            else:
                url += f'{k}={v}&'
        url = url[:-1] # strip away extra '&'

    # url = f'{API_URL_BASE}/coins/chainlink/history?id={id}&date={gecko_date}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return Response(json.loads(response.text))
    except HTTPError as err:
        err = {
            'error': f'{err}', 
            'detail': 'Required query params e.g ' 
                      '/marketCap?id=chainlink&date=30/12/2017&currency=gbp'
        }
        return Response(err, status=status.HTTP_404_NOT_FOUND)


# def _get_coin_history(params):
#     if not params.get('date'):
#         err = {
#             'detail': 'date query parameter is required',
#             'example': '/marketCap/chainlink?date=30/12/2017'
#         }
#         return Response(err, status=status.HTTP_400_BAD_REQUEST)

#     gecko_date = _convert_date(params.get('date'))
#     url = f'{API_URL_BASE}/coins/chainlink/history?id={id}&date={gecko_date}'
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         return Response(json.loads(response.text))
#     except HTTPError as err:
#         print(f'HTTP error: {err}')


# def _get_coin_list():
#     url = f'{API_URL_BASE}/coins/list'
#     response = requests.get(url)
#     response.raise_for_status()
#     return response


def _convert_date(datestring):
    date_string = '30/12/2017'
    format_string = '%d/%m/%Y'
    date_object = datetime.strptime(date_string, format_string)
    return date_object.strftime('%d-%m-%Y')
