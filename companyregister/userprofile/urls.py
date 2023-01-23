from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.account, name='account'),
    path('limits/<int:register>', views.check_limit, name='limit'),
    path('reset-limit', views.reset_limit, name='reset')
]
