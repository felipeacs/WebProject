import json
from datetime import timedelta, date

import pandas as pd
import requests as req
from bootstrap_modal_forms.generic import (
    BSModalCreateView
)
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ExecutionHistory
from .models import Executions


# Create your views here.


def home(request):
    text = 'Hello World!'
    return HttpResponse(text)


def dashboard(request):
    context = {
    }

    return render(request, 'dashboard_view.html', context)


def get_external_api(url):
    try:
        response = req.get(url)
        response_data = response.content.decode('utf-8')
    except Exception as e:
        response_data = {'Erro': 'Erro ao consultar API, favor contactar ao ADM!'}
    return response_data


def get_valid_external_api(url):
    try:
        response = req.get(url)
        response_content, response_status_code = response.content, response.status_code
    except Exception as e:
        response_content = {'Erro': 'Erro ao consultar API, favor contactar ao ADM!'}
        response_status_code = 500
    return response_content, response_status_code


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


class ExecutionsView(BSModalCreateView):
    template_name = 'dashboard/create_exec_hist.html'
    model = Executions
    form_class = ExecutionHistory
    success_message = 'Success'


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        data_request = self.request
        state = data_request.query_params.get('state')
        country = data_request.query_params.get('country')
        end_date = data_request.query_params.get('end_date')
        start_date = data_request.query_params.get('start_date')
        url_test = data_request.query_params.get('url_test')
        external_url_api_test = 'https://covid19-brazil-api.now.sh/api/status/v1'

        input_data = {
            "state": state,
            "country": country,
            "end_date": end_date,
            "start_date": start_date,
        }
        LST_ORDEM_ESCOPO = ['uf', 'state', 'cases', 'deaths', 'datetime']
        list_covid_uf = []
        list_covid_cases = []
        list_covid_state = []
        list_codid_date = []
        list_codiv_cases = []
        list_covid_deaths = []
        if url_test is not None:
            external_url_api_test = url_test

        url_list = prepara_url(input_data['country'], input_data['start_date'], input_data['end_date'])
        response_content, response_status_code = get_valid_external_api(external_url_api_test)
        if response_status_code == 200:
            data_frame_covid = [pd.DataFrame.from_dict(json.loads(get_external_api(url))['data']) for url in url_list]
            data_frame_covid_concat = pd.concat(data_frame_covid, ignore_index=True)
            data_frame_covid_out = data_frame_covid_concat[LST_ORDEM_ESCOPO]
            if input_data['state'] != '':
                data_frame_covid_out = data_frame_covid_out[(data_frame_covid_out.uf == input_data['state'])]
                for index, row in data_frame_covid_out.iterrows():
                    if row['uf'] == input_data['state']:
                        list_covid_uf.append(row['uf'])
                        list_covid_state.append(row['state'])
                        list_codid_date.append(row['datetime'])
                        list_codiv_cases.append(row['cases'])
                        list_covid_deaths.append(row['deaths'])
                list_covid_cases.append({"uf": list_covid_uf[0],
                                         "state": list_covid_state[0],
                                         "datetime": list_codid_date,
                                         "cases": list_codiv_cases,
                                         "deaths": list_covid_deaths})
        else:
            list_covid_cases.append(
                {"uf": 0,
                 "state": 0,
                 "datetime": list_codid_date,
                 "cases": list_codiv_cases,
                 "deaths": list_covid_deaths,
                 "Erro": "Erro ao consultar API externa."}
            )

        return Response(list_covid_cases)
