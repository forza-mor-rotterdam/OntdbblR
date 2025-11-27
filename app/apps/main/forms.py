from apps.main.models import Regel
from apps.main.services import OnderwerpenService
from django import forms


class RegelChangeForm(forms.ModelForm):
    deduplicate = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        ),
        label="Deduplicate",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Regel
        fields = (
            "deduplicate",
            "distance",
            "max_age",
        )


class RegelCreateForm(forms.ModelForm):
    deduplicate = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        ),
        label="Deduplicate",
        required=False,
    )

    onderwerp_url = forms.ChoiceField(
        widget=forms.RadioSelect(
            attrs={
                "class": "list--form-radio-input",
            }
        ),
        choices=(),
        label="Onderwerp",
        required=True,
    )

    class Meta:
        model = Regel
        fields = (
            "onderwerp_url",
            "deduplicate",
            "distance",
            "max_age",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        onderwerpen_service = OnderwerpenService()

        bestaande_onderwerp_urls = list(
            Regel.objects.values_list("onderwerp_url", flat=True)
        )
        groepen = onderwerpen_service.get_groepen(force_cache=True)
        groepnaam_door_uuid = {g.get("uuid"): g.get("name") for g in groepen}
        onderwerpen = onderwerpen_service.get_onderwerpen(force_cache=True)
        self.fields["onderwerp_url"].choices = [
            (
                o.get("_links", {}).get("self"),
                f"{groepnaam_door_uuid.get(o.get('group_uuid'), o.get('group_uuid'))} - {o.get('name')}",
            )
            for o in onderwerpen
            if o.get("_links", {}).get("self") not in bestaande_onderwerp_urls
        ]
