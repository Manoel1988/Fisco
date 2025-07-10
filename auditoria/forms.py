# auditoria/forms.py

from django import forms
from .models import DocumentoFiscal, Empresa

class DocumentoFiscalForm(forms.ModelForm):
    class Meta:
        model = DocumentoFiscal
        fields = ['empresa', 'tipo_documento', 'mes', 'ano', 'arquivo']
        # Se quiser esconder empresa, tipo_documento, mes, ano e preencher via view
        # fields = ['arquivo']

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'razao_social', 'cnpj', 'regime_tributario',
            'atividade_principal', 'cnae_principal',
            'principais_ncm', 'produtos_principais',
            'faturamento_anual', 'numero_funcionarios',
            'tem_filiais', 'estados_operacao',
            'exporta', 'importa',
            'tem_beneficios_fiscais', 'quais_beneficios',
            'regime_apuracao', 'setor_atuacao',
            'tem_gastos_pd', 'tem_gastos_treinamento', 'tem_gastos_ambientais',
            'usa_pj', 'usa_terceirizacao',
            'observacoes_fiscais',
            
            # Localização
            'cidade',
            'estado', 
            'uf',
            'cep',
        ]
        widgets = {
            'razao_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: EMPRESA EXEMPLO LTDA'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 12.345.678/0001-90'}),
            'regime_tributario': forms.Select(attrs={'class': 'form-control'}),
            'atividade_principal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Consultoria em tecnologia da informação'}),
            'cnae_principal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 6201-5'}),
            'principais_ncm': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1234.56.78, 9876.54.32'}),
            'produtos_principais': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descreva os principais produtos que a empresa comercializa'}),
            'faturamento_anual': forms.Select(attrs={'class': 'form-control'}),
            'numero_funcionarios': forms.Select(attrs={'class': 'form-control'}),
            'estados_operacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: SP, RJ, MG'}),
            'quais_beneficios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descreva os benefícios fiscais que a empresa possui'}),
            'regime_apuracao': forms.Select(attrs={'class': 'form-control'}),
            'setor_atuacao': forms.Select(attrs={'class': 'form-control'}),
            'observacoes_fiscais': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Observações importantes sobre a situação fiscal da empresa'}),
            
            # Localização
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: São Paulo'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: São Paulo'}),
            'uf': forms.Select(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 12345-678'}),
        }
        labels = {
            'razao_social': 'Razão Social',
            'cnpj': 'CNPJ',
            'regime_tributario': 'Regime Tributário',
            'atividade_principal': 'Atividade Principal',
            'cnae_principal': 'CNAE Principal',
            'principais_ncm': 'Principais NCM',
            'produtos_principais': 'Principais Produtos',
            'faturamento_anual': 'Faturamento Anual',
            'numero_funcionarios': 'Número de Funcionários',
            'tem_filiais': 'Possui Filiais?',
            'estados_operacao': 'Estados onde Opera',
            'exporta': 'Realiza Exportações?',
            'importa': 'Realiza Importações?',
            'tem_beneficios_fiscais': 'Possui Benefícios Fiscais?',
            'quais_beneficios': 'Quais Benefícios Fiscais?',
            'regime_apuracao': 'Regime de Apuração',
            'setor_atuacao': 'Setor de Atuação',
            'tem_gastos_pd': 'Possui Gastos com P&D?',
            'tem_gastos_treinamento': 'Possui Gastos com Treinamento?',
            'tem_gastos_ambientais': 'Possui Gastos Ambientais?',
            'usa_pj': 'Contrata Pessoa Jurídica (PJ)?',
            'usa_terceirizacao': 'Usa Serviços Terceirizados?',
            'observacoes_fiscais': 'Observações Fiscais',
            
            # Localização
            'cidade': 'Cidade',
            'estado': 'Estado',
            'uf': 'UF',
            'cep': 'CEP',
        }
        
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj:
            # Remove formatação do CNPJ
            cnpj = ''.join(filter(str.isdigit, cnpj))
            if len(cnpj) != 14:
                raise forms.ValidationError("CNPJ deve ter 14 dígitos.")
            # Formata o CNPJ
            cnpj = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
        return cnpj
    
    def clean_cnae_principal(self):
        cnae = self.cleaned_data.get('cnae_principal')
        if cnae:
            # Remove formatação
            cnae = ''.join(filter(str.isdigit, cnae))
            if len(cnae) == 7:
                # Formata o CNAE: 1234567 -> 1234-5/67
                cnae = f"{cnae[:4]}-{cnae[4]}/{cnae[5:]}"
        return cnae
    
    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        if cep:
            # Remove formatação do CEP
            cep = ''.join(filter(str.isdigit, cep))
            if len(cep) != 8:
                raise forms.ValidationError("CEP deve ter 8 dígitos.")
            # Formata o CEP
            cep = f"{cep[:5]}-{cep[5:]}"
        return cep