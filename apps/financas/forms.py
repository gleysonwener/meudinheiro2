from django import forms

from .models import Categoria, Receita, Despesa


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        exclude = ['usuario']


class ReceitaForm(forms.ModelForm):

    class Meta:
        model = Receita
        exclude = ['usuario']



class DespesaForm(forms.ModelForm):

    class Meta:
        model = Despesa
        exclude = ['usuario']

