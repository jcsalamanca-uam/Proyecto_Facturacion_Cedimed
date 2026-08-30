from django import forms
from django.forms import inlineformset_factory

from .models import Factura, LineaFactura


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ["numero", "cliente", "fecha", "vence", "estado", "observaciones"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "vence": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }


LineaFacturaFormSet = inlineformset_factory(
    Factura,
    LineaFactura,
    fields=("producto", "descripcion", "cantidad", "precio_unitario", "iva"),
    extra=3,
    can_delete=True,
)
