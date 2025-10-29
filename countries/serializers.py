from rest_framework import serializers
from .models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
        read_only_fields = ("id", "last_refreshed_at", "estimated_gdp", "exchange_rate")

    def validate(self, data):
        """
        Validate required fields for manual country creation.
        Returns proper error format for missing fields.
        """
        # Only validate on create (not update)
        if self.instance is None:
            required_fields = {
                "name": "name",
                "population": "population",
                "currency_code": "currency_code"
            }
            
            errors = {}
            for field_name, display_name in required_fields.items():
                if not data.get(field_name):
                    errors[display_name] = "is required"
            
            if errors:
                raise serializers.ValidationError(errors)
                
        return data
