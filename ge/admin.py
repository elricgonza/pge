from django.contrib import admin
from ge.models import *

@admin.register(Continente)
class Continente(admin.ModelAdmin):
    fields = ('nom_continente',)
    #search_fields = ('ut', 'nombre')
    list_display = ('nom_continente', 'id')

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    fields = ('nom_pais', 'nom_pais_inter', 'nom_pais_alias', 'iso3166_2', 'iso3166_3', 'nacionalidad', 'periodo_ini', 'periodo_fin', 'actual', 'descripcion', 'estado', 'continente', 'fecha_ingreso', 'lat_ref', 'long_ref', 'geohash_ref')
    search_fields = ('nom_pais', 'continente')
    list_display = ('id', 'nom_pais', 'continente')

@admin.register(Ut_sup)
class Ut_supAdmin(admin.ModelAdmin):
    search_fields = ('nom_ut_sup', 'pais')
    list_display = ('id', 'nom_ut_sup', 'pais')

@admin.register(Ut_intermedia)
class Ut_intermediaAdmin(admin.ModelAdmin):
    search_fields = ('nom_ut_intermedia', 'ut_sup')
    list_display = ('id', 'nom_ut_intermedia', 'ut_sup')

@admin.register(Ut_basica)
class Ut_basicaAdmin(admin.ModelAdmin):
    search_fields = ('nom_ut_basica', 'ut_intermedia')
    list_display = ('id', 'nom_ut_basica', 'ut_intermedia')

@admin.register(Localidad)
class LocalidadAdmin(admin.ModelAdmin):
    search_fields = ('nom_localidad', 'ut_basica')
    list_display = ('id', 'nom_localidad', 'ut_basica')

@admin.register(Nivel_ut)
class Nivel_utAdmin(admin.ModelAdmin):
    search_fields = ('ut_descripcion', 'pais')
    list_display = ('id', 'ut_descripcion', 'pais')
