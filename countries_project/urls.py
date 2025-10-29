"""
URL configuration for countries_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from countries.views import (
    RefreshCountriesView,
    CountryListView,
    CountryCreateView,
    CountryDetailView,
    StatusView,
    SummaryImageView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Country CRUD endpoints
    path('countries/refresh', RefreshCountriesView.as_view(), name='refresh-countries'),
    path('countries/image', SummaryImageView.as_view(), name='summary-image'),
    path('countries/<str:name>', CountryDetailView.as_view(), name='country-detail'),
    path('countries', CountryListView.as_view(), name='country-list'),
    
    # Status endpoint
    path('status', StatusView.as_view(), name='status'),
]
