import os
import random

import requests
from django.conf import settings
from django.db import transaction
from django.utils.timezone import now
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CountrySerializer
from .models import Country
from django.http import FileResponse
from .models import Country, RefreshStatus
from .utils import generate_summary_image


COUNTRIES_API = "https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies"
EXCHANGE_API = "https://open.er-api.com/v6/latest/USD"


class RefreshCountriesView(APIView):
    """
    API view to refresh country data from external sources.
    
    Fetches country information and exchange rates, then updates the database.
    """
    
    def post(self, request):
        """
        Handle POST request to refresh country data.
        
        Returns:
            Response: JSON response with refresh status and statistics
        """
        # Fetch data from external APIs
        try:
            r_c = requests.get(COUNTRIES_API, timeout=15)
            r_e = requests.get(EXCHANGE_API, timeout=15)
        except requests.RequestException:
            return Response(
                {
                    "error": "External data source unavailable",
                    "details": "Could not fetch data from Countries or Exchange API",
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        if r_c.status_code != 200:
            return Response(
                {
                    "error": "External data source unavailable",
                    "details": "Could not fetch data from Countries API",
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        try:
            countries_data = r_c.json()
            exchange_data = r_e.json()
            rates = exchange_data.get("rates") or exchange_data.get("conversion_rates") or {}
        except ValueError:
            return Response(
                {"error": "External data source unavailable", "details": "Invalid JSON from APIs"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        with transaction.atomic():
            processed = []

            for c in countries_data:
                name = c.get("name")
                capital = c.get("capital")
                region = c.get("region")
                population = c.get("population") or 0
                flag_url = c.get("flag") or (
                    c.get("flags", {}).get("svg") if isinstance(c.get("flags"), dict) else None
                )
                currencies = c.get("currencies") or []

                currency_code = None
                exchange_rate = None
                estimated_gdp = None

                if currencies:
                    first = currencies[0]
                    currency_code = first.get("code") if isinstance(first, dict) else None

                if currency_code:
                    rate = rates.get(currency_code)
                    if rate is not None:
                        try:
                            exchange_rate = float(rate)
                            multiplier = random.uniform(1000, 2000)
                            if exchange_rate > 0:
                                estimated_gdp = (population * multiplier) / exchange_rate
                        except Exception:
                            exchange_rate = None
                            estimated_gdp = None

                defaults = {
                    "capital": capital or None,
                    "region": region or None,
                    "population": population,
                    "currency_code": currency_code,
                    "exchange_rate": exchange_rate,
                    "estimated_gdp": estimated_gdp,
                    "flag_url": flag_url,
                }

                # Update if exists, otherwise create
                try:
                    existing = Country.objects.get(name__iexact=name)
                    for k, v in defaults.items():
                        setattr(existing, k, v)
                    existing.save()
                    obj = existing
                    created = False
                except Country.DoesNotExist:
                    obj = Country.objects.create(name=name, **defaults)
                    created = True

                processed.append(obj)

        total = Country.objects.count()
        rs, _ = RefreshStatus.objects.update_or_create(id=1)
        rs.total_countries = total
        rs.last_refreshed_at = now()
        rs.save()

        # Generate summary image
        top5 = Country.objects.filter(estimated_gdp__isnull=False).order_by('-estimated_gdp')[:5]
        output_path = os.path.join(settings.BASE_DIR, 'cache', 'summary.png')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        generate_summary_image(total, list(top5), rs.last_refreshed_at, output_path=output_path)

        return Response(
            {
                "message": "Countries refreshed successfully",
                "total_countries": total,
            },
            status=status.HTTP_200_OK,
        )

class CountryListView(APIView):
    """
    Get all countries with optional filters and sorting.
    Returns a plain array (not paginated) to match task requirements.
    """
    
    def get(self, request):
        qs = Country.objects.all()
        
        # Apply filters
        region = request.query_params.get('region')
        currency = request.query_params.get('currency')
        sort = request.query_params.get('sort')

        if region:
            qs = qs.filter(region__iexact=region)
        if currency:
            qs = qs.filter(currency_code__iexact=currency)
        if sort == 'gdp_desc':
            qs = qs.order_by('-estimated_gdp')
        elif sort == 'gdp_asc':
            qs = qs.order_by('estimated_gdp')
        
        serializer = CountrySerializer(qs, many=True)
        # Return plain array, not paginated response
        return Response(serializer.data, status=status.HTTP_200_OK)


class CountryCreateView(APIView):
    """
    Manual endpoint to create a country with proper validation.
    """
    
    def post(self, request):
        """
        Create a new country manually with validation.
        
        Returns validation errors in the format:
        {
            "error": "Validation failed",
            "details": {
                "field_name": "is required"
            }
        }
        """
        serializer = CountrySerializer(data=request.data)
        
        if not serializer.is_valid():
            # Format errors to match the required structure
            return Response(
                {
                    "error": "Validation failed",
                    "details": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CountryDetailView(APIView):
    def get(self, request, name):
        try:
            c = Country.objects.get(name__iexact=name)
        except Country.DoesNotExist:
            return Response(
                {"error": "Country not found"},
                status=status.HTTP_404_NOT_FOUND)
        serializer = CountrySerializer(c) 
        return Response(serializer.data)
    
    def delete(self, request, name):
        try:
            c = Country.objects.get(name__iexact=name)
        except Country.DoesNotExist:
            return Response(
                {"error": "Country not found"},
                status=status.HTTP_404_NOT_FOUND)
        c.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class StatusView(APIView):
    def get(self, request):
        rs = RefreshStatus.objects.filter(id=1).first()
        if not rs or not rs.last_refreshed_at:
            return Response({"total_countries": 0, "last_refreshed_at": None})
        return Response({
                "total_countries": rs.total_countries,
                "last_refreshed_at": rs.last_refreshed_at.isoformat()
            }
        )
    
class SummaryImageView(APIView):
    def get(self, request):
        path = os.path.join(settings.BASE_DIR, 'cache', 'summary.png')
        if not os.path.exists(path):
            return Response(
                {"error": "Summary image not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        return FileResponse(open(path, 'rb'), content_type='image/png')