# -*- coding: utf-8 -*-
#!python
#log/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from ge.forms import Categoria
from ge.forms import CategoriaForm
from ge.forms import SearchForm
from ge.models import Recinto

# Create your views here.
# this login required decorator is to not allow to any
# view without authenticating
@login_required(login_url="login/")
def home(request):
	return render(request,"home.html")


def categoria_new(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.nom_categoria = form.cleaned_data['nom_categoria']
            categoria.save()
            #return redirect('categoria_detail', pk=categoria.pk)
    else:
        form = CategoriaForm()
    return render(request, 'categoria_edit.html', {'form': form})


def search_page(request):
    form = SearchForm()
    recintos = []
    show_results = False
    if request.GET.has_key('txt_search'):
        show_results = True
        txt_search = request.GET['txt_search'].strip()
        if txt_search:
            form = SearchForm({'txt_search' : txt_search })
            recintos = Recinto.objects.filter (nom_recinto__icontains=txt_search)[:10]
    variables = RequestContext(request, {
        'form': form,
        'recintos': recintos,
        'show_results': show_results
    })
    return render_to_response('search.html', variables)



