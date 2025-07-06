# auditoria/forms.py

from django import forms
from .models import DocumentoFiscal

class DocumentoFiscalForm(forms.ModelForm):
    class Meta:
        model = DocumentoFiscal
        fields = ['empresa', 'tipo_documento', 'mes', 'ano', 'arquivo']
        # Se quiser esconder empresa, tipo_documento, mes, ano e preencher via view
        # fields = ['arquivo']