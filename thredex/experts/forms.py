from django import forms
from cities_light.models import City, Country
from .models import Location

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['country', 'city']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country = self.data.get('country')
                self.fields['city'].queryset = City.objects.filter(country__code2=country).order_by('name')
            except (ValueError, TypeError):
                pass  # Invalid country, show no cities

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if not country:
            raise forms.ValidationError("Please select a country.")
        return country

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if not city:
            raise forms.ValidationError("Please select a city.")
        return city
