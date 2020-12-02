import json
from datetime import timedelta, date

import pandas as pd
import requests as req
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.


def home(request):
    text = 'Hello World!'
    return HttpResponse(text)


def get_external_api(url):
    try:
        response = req.get(url)
        response_data = response.content.decode('utf-8')
    except Exception as e:
        response_data = {'Erro': 'Erro ao consultar API, favor contactar ao ADM!'}
    return response_data


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def prepara_url(country, start_date, end_date):
    url = 'https://covid19-brazil-api.now.sh/api/report/v1/{}/{}/'
    start_yyyy, start_mm, start_dd = int(start_date[:4]), int(start_date[4:6]), int(start_date[6:8])
    end_yyyy, end_mm, end_dd = int(end_date[:4]), int(end_date[4:6]), int(end_date[6:8])
    start_dt = date(start_yyyy, start_mm, start_dd)
    end_dt = date(end_yyyy, end_mm, end_dd)
    if end_date != start_date:
        date_list = [date.strftime("%Y%m%d") for date in date_range(start_dt, end_dt)]
        url_list = [url.format(country, date) for date in date_list]
    else:
        url_list = [url.format(country, start_date)]
    return url_list


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        data_request = self.request
        state = data_request.query_params.get('state')
        country = data_request.query_params.get('country')
        end_date = data_request.query_params.get('end_date')
        start_date = data_request.query_params.get('start_date')

        input_data = {
            "state": state,
            "country": country,
            "end_date": end_date,
            "start_date": start_date,
        }

        url_list = prepara_url(input_data['country'], input_data['start_date'], input_data['end_date'])
        data_frame_covid = [pd.DataFrame.from_dict(json.loads(get_external_api(url))) for url in url_list]
        data_frame_covid_concat = pd.concat(data_frame_covid, ignore_index=True)
        result_data_json = data_frame_covid_concat.to_json(force_ascii=False, orient="index")
        parsed = json.loads(result_data_json, encoding='utf-8')
        result_data = json.dumps(parsed, ensure_ascii=False)

        return Response(eval(result_data))
