from django import forms

from .constants import TEAM_PART_MAPPING
from .models import Assembly, Part


class PartForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user_team = kwargs.pop("user_team", None)
        super(PartForm, self).__init__(*args, **kwargs)
        if self.user_team:
            allowed_part_types = TEAM_PART_MAPPING.get(self.user_team.name, [])
            self.fields["part_type"].choices = [(pt, pt) for pt in allowed_part_types]

    class Meta:
        model = Part
        fields = ["part_type", "aircraft", "stock"]
        widgets = {
            "part_type": forms.Select(attrs={"class": "form-select"}),
            "aircraft": forms.Select(attrs={"class": "form-select"}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }

    def clean(self):
        cleaned_data = super().clean()
        part_type = cleaned_data.get("part_type")
        aircraft = cleaned_data.get("aircraft")
        team = self.user_team

        if part_type and aircraft and team:
            # Check if a part with this combination already exists by excluding the current instance (for create/update distinction)
            duplicate_qs = Part.objects.filter(part_type=part_type, aircraft=aircraft, team=team)
            if self.instance.pk:
                duplicate_qs = duplicate_qs.exclude(pk=self.instance.pk)
            if duplicate_qs.exists():
                raise forms.ValidationError(
                    "A part of this type for the selected aircraft already exists. Please edit the existing part."
                )
        return cleaned_data


class AssemblyForm(forms.ModelForm):
    class Meta:
        model = Assembly
        fields = ["aircraft"]
        widgets = {
            "aircraft": forms.Select(attrs={"class": "form-select"}),
        }
