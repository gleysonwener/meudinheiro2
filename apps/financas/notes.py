from itertools import count

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Categoria, Receita, Despesa

from .forms import CategoriaForm, ReceitaForm, DespesaForm

from django.db.models import Count, Sum

@login_required
def principal(request):
    template_name = 'financas/principal.html'

    total_receitas = Receita.objects.filter(usuario=request.user)
    total_despesas = Despesa.objects.filter(usuario=request.user)
    total_categorias = Categoria.objects.filter(usuario=request.user)
    ultimas_receitas = Receita.objects.filter(usuario=request.user).order_by('-id')[:3]
    ultimas_despesas = Despesa.objects.filter(usuario=request.user).order_by('-id')[:3]
    ultimas_categorias = Categoria.objects.filter(usuario=request.user).order_by('-id')[:3]

    context = {
        'ultimas_receitas': ultimas_receitas,
        'ultimas_despesas': ultimas_despesas,
        'ultimas_categorias': ultimas_categorias,
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'total_categorias': total_categorias,
    }

    return render(request, template_name, context)


@login_required
def nova_categoria(request):
    template_name = 'financas/nova_categoria.html'
    context = {}
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            cat_form = form.save(commit=False)
            cat_form.usuario = request.user
            cat_form.save()
            messages.success(request, 'Categoria adicionada com sucesso.')
            return redirect('financas:lista_categorias')

    else:
        form = CategoriaForm()
    context['form'] = form
    return render(request, template_name, context)


@login_required
def lista_categorias(request):
    template_name = 'financas/lista_categorias.html'
    #categorias = Categoria.objects.all() # raw - para usar comandos sql
    categorias = Categoria.objects.filter(usuario=request.user) # raw - para usar comandos sql
    context = {
        'categorias': categorias
    }
    return render(request, template_name, context)


@login_required
def editar_categoria(request, pk):
    template_name = 'financas/nova_categoria.html'
    context = {}
    #categoria = get_object_or_404(Categoria, id=pk)
    #categoria = Categoria.objects.filter(pk=pk, usuario=request.user).first()

    try:
        categoria = Categoria.objects.get(pk=pk, usuario=request.user) # ORM-> SELECT * FROM categoria WHERE id=pk
    except Categoria.DoesNotExist as e:
        messages.warning(request, 'Voçê não tem permissão para editar a categoria informada.')
        return redirect('financas:lista_categorias')

    if request.method =='POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso.')
            return redirect('financas:lista_categorias')

    else:
        form = CategoriaForm(instance=categoria)
    context['form'] = form
    return render(request, template_name, context)


@login_required
def apagar_categoria(request, pk):
    try:
        categoria = Categoria.objects.get(pk=pk, usuario=request.user)  # ORM-> SELECT * FROM categoria WHERE id=pk
        categoria.delete()
    except Categoria.DoesNotExist as e:
        messages.warning(request, 'Voçê não tem permissão para editar a categoria informada.')
        return redirect('financas:lista_categorias')
    messages.info(request, 'Categoria Apagada.')
    return redirect('financas:lista_categorias')


@login_required
def nova_receita(request):
    template_name = 'financas/nova_receita.html'
    context = {}
    if request.method == 'POST':
        form = ReceitaForm(data=request.POST, user=request.user)
        if form.is_valid():
            receita_form = form.save(commit=False)
            receita_form.usuario = request.user
            receita_form.save()
            messages.success(request, 'Receita adicionada com sucesso')
            return redirect('financas:lista_receitas')
    else:
        form = ReceitaForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)

@login_required
def lista_receitas(request):
    template_name = 'financas/lista_receitas.html'
    receitas = Receita.objects.filter(usuario=request.user)
    context = {
        'receitas': receitas
    }
    return render(request, template_name, context)


@login_required
def editar_receita(request, pk):
    template_name = 'financas/nova_receita.html'
    context = {}
    try:
        receita = Receita.objects.get(pk=pk, usuario=request.user)
    except Receita.DoesNotExist as e:
        messages.warning(request, 'Você não tem permissão para editar a receita informada.')
        return redirect('financas:lista_receitas')

    if request.method == 'POST':
        form = ReceitaForm(data=request.POST, instance=receita, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Receita atualizada com suceso.')
            return redirect('financas:lista_receitas')
    else:
        form = ReceitaForm(instance=receita, user=request.user)
    context['form'] = form
    return render(request, template_name, context)


@login_required
def apagar_receita(request, pk):
    try:
        receita = Receita.objects.get(pk=pk, usuario=request.user)
        receita.delete()
    except Receita.DoNotExist as e:
        messages.warning(request, 'Você não tem permissão para apagar a receita informada.')
        return redirect('financas:lista_receitas')

    messages.info(request, 'Receita Apagada.')
    return redirect('financas:lista_receitas')


@login_required
def lista_despesas(request):
    template_name = 'financas/lista_despesas.html'
    despesas = Despesa.objects.filter(usuario=request.user)
    context = {
        'despesas': despesas
    }
    return render(request, template_name, context)


@login_required
def nova_despesa(request):
    template_name = 'financas/nova_despesa.html'
    context = {}
    if request.method == 'POST':
        form = DespesaForm(data=request.POST, user=request.user)
        if form.is_valid():
            despesa_form = form.save(commit=False)
            despesa_form.usuario = request.user
            despesa_form.save()
            messages.success(request, 'Despesa adicionada com sucesso.')
            return redirect('financas:lista_despesas')
    else:
        form = DespesaForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)


@login_required
def editar_despesa(request, pk):
    template_name = 'financas/nova_despesa.html'
    context = {}
    try:
        despesa = Despesa.objects.get(pk=pk, usuario=request.user)
    except Despesa.DoesNotExist as e:
        messages.warning(request, 'Você não tem permissao para editar a depea informada.')
        return redirect('financas:lista_despesas')

    if request.method == 'POST':
        form = DespesaForm(data=request.POST, instance=despesa, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Receita atualizada com sucesso')
            return redirect('financas:lista_despesas')
    else:
        form = DespesaForm(instance=despesa, user=request.user)
    context['form'] = form
    return render(request, template_name, context)


@login_required
def apagar_despesa(request, pk):
    try:
        despesa = Despesa.objects.get(pk=pk, usuario=request.user)
        despesa.delete()
    except Despesa.DoNotExist as e:
        messages.warning(request, 'Você não tem permissão para apagar a despesa informada')
        return redirect('financas:lista_despesas')
    messages.info(request, 'Despesa Apagada.')
    return redirect('financas:lista_despesas')



termo_busca = request.GET.get('pesquisa', None)

    if termo_busca:
        categoria = Categoria.objects.all()
        categoria = Categoria.objects.filter(nome__icontains=termo_busca)
    else:
        categoria = Categoria.objects.all()
