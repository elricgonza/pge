#!python
#log/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ge.forms import Categoria
from ge.forms import CategoriaForm

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
            #categoria.nom_categoria = request.nom_categoria
            categoria.nom_categoria = form.cleaned_data['nom_categoria']
            categoria.save()
            #return redirect('categoria_detail', pk=categoria.pk)
    else:
        form = CategoriaForm()
    return render(request, 'categoria_edit.html', {'form': form})
