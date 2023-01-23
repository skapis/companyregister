from django.shortcuts import render
from .functions import get_company, get_entrepreneur
from django.contrib.auth.decorators import login_required
from userprofile.models import APILimits
from django.http import JsonResponse
import json



def homepage(request):
    return render(request, 'homepage.html')


@login_required(login_url='/auth/login')
def dashboard(request):
    apis = APILimits.objects.filter(owner=request.user).order_by('id')

    context = {
        'apis': apis
    }
    return render(request, 'company/index.html', context)


@login_required(login_url='/auth/login')
def ares(request):
    return render(request, 'company/ares.html')


@login_required(login_url='/auth/login')
def res(request):
    return render(request, 'company/res.html')


@login_required(login_url='/auth/login')
def get_companies_ares(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        companies = data['companyList']
        output = []
        limit = APILimits.objects.get(owner=request.user, registerName=1)
        for company in companies:
            if limit.limit != 0:
                limit.limit = limit.limit - 1
                limit.save()
                if len(company) == 8:
                    company_data = get_company(company)
                    if 'error' not in company_data.keys():
                        output.append(company_data)

            response = {
                'requested': companies.__len__(),
                'fetched': output.__len__(),
                'data': output
            }
    return JsonResponse(response, status=200)


def get_entrepreneurs_res(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        entrepreneurs = data['companyList']
        output = []
        limit = APILimits.objects.get(owner=request.user, registerName=2)
        for entrepreneur in entrepreneurs:
            if limit.limit != 0:
                limit.limit = limit.limit - 1
                limit.save()
                if len(entrepreneur) == 8:
                    entrepreneur_data = get_entrepreneur(entrepreneur)
                    if 'error' not in entrepreneur_data.keys():
                        output.append(entrepreneur_data)

            response = {
                'requested': entrepreneur.__len__(),
                'fetched': output.__len__(),
                'data': output
            }
        return JsonResponse(response, status=200)
