from django import forms

class ShortenForm(forms.Form):
    original_url = forms.URLField(
        label="Long URL",
        widget=forms.URLInput(attrs={"class":"form-control","placeholder":"https://example.com/very/long/link"})
    )
    custom_code = forms.SlugField(
        label="Custom code (optional)",
        required=False, max_length=16,
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":"e.g., my-offer"})
    )
    expires_in_days = forms.IntegerField(
        label="Expire after (days)",
        required=False, min_value=1, max_value=365,
        widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"7"})
    )
