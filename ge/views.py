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


def recinto_detail(request, pk):
    recinto = get_object_or_404(Recinto, pk=pk)
    return render(request, 'recinto_detail.html', {'recinto': recinto})


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
            #recintos = Recinto.objects.filter(nom_recinto__icontains=txt_search)[:10]
            txt_search= '%'+txt_search+'%'
            recintos = Recinto.objects.raw('''
                select a.id, a.nom_recinto, a.direccion, b.zona as zona2, c.distrito, e.nom_asiento,
                        f.nom_ut_basica, g.nom_ut_intermedia, h.nom_ut_sup, i.nom_pais, j.nom_continente
                from ge_recinto a
                left join  ge_zona b on a.zona_id = b.id
                left join  ge_distrito c on b.distrito_id = c.id
                left join  ge_asiento_distrito  d on c.id  = d.distrito_id
                left join  ge_asiento  e on e.id = d.asiento_id
                left join g_ut_basica f on e.ut_basica_id = f.id
                left join g_ut_intermedia g on f.ut_intermedia_id = g.id
                left join g_ut_sup h on g.ut_sup_id = h.id
                left join g_pais i on h.pais_id = i.id
                left join g_continente j on i.continente_id = j.id
                where a.nom_recinto ilike %s ''', [txt_search])

            """
            recintos = Recinto.objects.raw(''' select a.id, a.nom_recinto, a.direccion, b.zona as zona2
                                           from ge_recinto a
                                           left join ge_zona b on a.zona_id = b.id
                                           where nom_recinto ilike  %s ''', [txt_search])
            """
    variables = RequestContext(request, {
                'form': form,
                'recintos': recintos,
                'show_results': show_results
    })
    return render_to_response('search.html', variables)
