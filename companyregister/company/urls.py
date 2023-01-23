from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('ares', views.ares, name='ares_index'),
    path('res', views.res, name='res_index'),
    path('ares/company/bulk', views.get_companies_ares, name='ares_bulk'),
    path('res/entrepreneurs/bulk', views.get_entrepreneurs_res, name='res_bulk')
]
