from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import APILimits, Register
from django.http import JsonResponse
from datetime import datetime


@login_required(login_url='/auth/login')
def account(request):
    if request.method == 'GET':
        limits = APILimits.objects.filter(owner=request.user)
        context = {
            'apis': limits
        }
        return render(request, 'user/index.html', context)


@login_required(login_url='/auth/login')
def check_limit(request, register):
    if request.method == 'GET':
        limits = APILimits.objects.filter(owner=request.user, registerName=register)
        return JsonResponse(list(limits.values()), status=200, safe=False)


@login_required(login_url='/auth/login')
def reset_limit(request):
    if request.method == 'GET':
        limits = APILimits.objects.filter(owner=request.user)
        for limit in limits:
            if limit.resetDate != datetime.now().date():
                register = Register.objects.get(name=limit.registerName)
                limit.limit = register.limit
                limit.resetDate = datetime.now().date()
                limit.save()
    return JsonResponse({'result': 'Limits were updated'}, status=200)
