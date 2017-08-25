# -*- coding: utf-8 -*-
from django.contrib import admin
from ge.models import *
from django.contrib.admin import AdminSite


AdminSite.site_title = 'OEP'
AdminSite.site_header = 'OEP-Geografía Electoral'
AdminSite.index_title = 'Administración-BD'


@admin.register(Continente)
class Continente(admin.ModelAdmin):
    fields = ('nom_continente',)
    #search_fields = ('ut', 'nombre')
    list_display = ('nom_continente', 'id')


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    fields = ('id_origen', 'version', 'nom_pais', 'nom_pais_inter', 'nom_pais_alias', 'iso3166_2', 'iso3166_3', 'nacionalidad', 'periodo_ini', 'periodo_fin', 'actual', 'descripcion', 'estado', 'continente', 'fecha_ingreso', 'lat_ref', 'long_ref', 'geohash_ref')
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


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    exclude = ('geom',)


class Asiento_jurisdiccionInline(admin.TabularInline):
    model = Asiento_jurisdiccion
    extra = 1

    def get_extra (self, request, obj=None, **kwargs):
        #Dynamically sets the number of extra forms. 0 if the related object
        #already exists or the extra configuration otherwise.
        if obj:
            # Don't add any extra forms if the related object already exists.
            return 0
        return self.extra


class RutaInline(admin.TabularInline):
    model = Ruta
    extra = 1

    def get_extra (self, request, obj=None, **kwargs):
        #Dynamically sets the number of extra forms. 0 if the related object
        #already exists or the extra configuration otherwise.
        if obj:
            # Don't add any extra forms if the related object already exists.
            return 0
        return self.extra


class Asiento_circunInline(admin.TabularInline):
    model = Asiento_circun
    extra = 1


class Asiento_imgInline(admin.TabularInline):
    model = Asiento_img


class Asiento_detalleInline(admin.TabularInline):
    model = Asiento_detalle


@admin.register(Asiento)
class AsientoAdmin(admin.ModelAdmin):
    list_filter = ('ut_basica',)
    search_fields = ('nom_asiento', 'ut_basica')
    list_display = ('id', 'nom_asiento', 'ubicacion')
    exclude = ('fecha_act', 'geom')
    readonly_fields = ('fecha_ingreso', 'fecha_act')
    inlines = (Asiento_circunInline, Asiento_detalleInline, Asiento_imgInline, RutaInline, Asiento_jurisdiccionInline)

    '''
    fields = [('continente_id', 'pais_id', 'ut_sup_id'),('ut_intermedia_id', 'ut_basica_id', 'localidad_id'),
             ('nom_asiento', 'resol_creacion', 'fecha_creacion')
             ]
    '''
    fieldsets = (
        ('Datos Ubicación Geográfica', {
            'fields': ('continente', 'pais', 'ut_sup', 'ut_intermedia', 'ut_basica', 'localidad',
                           ('latitud', 'longitud', 'geohash')
                      )
        }),
        ('Datos del Asiento Electoral', {'fields': ('nom_asiento', 'doc_actualizacion', 'fecha_doc_actualizacion', 'estado',
                          'proceso_activo', 'etapa', 'fecha_ingreso', 'obs', 'descripcion_ubicacion'
                          )
        }),
        ('Datos si existe Oficialía de Registro Civil', {'fields':('existe_orc', 'numero_orc')
        }),
    )


@admin.register(Distrito)
class DistritoAdmin(admin.ModelAdmin):
    search_fields = ('distrito', 'fecha_ingreso', 'id')
    list_display = ('id', 'distrito', 'fecha_ingreso')


@admin.register(Asiento_distrito)
class Asiento_distritoAdmin(admin.ModelAdmin):
    search_fields = ('distrito', 'asiento')
    list_display = ('id', 'distrito', 'asiento')


@admin.register(Asiento_img)
class Asiento_imgAdmin(admin.ModelAdmin):
    search_fields = ('asiento', )
    list_display = ('id', 'asiento', 'vista', 'img')



@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    search_fields = ('zona', 'distrito')
    list_display = ('id', 'zona', 'distrito')


@admin.register(Recinto)
class RecintoAdmin(admin.ModelAdmin):
    search_fields = ('nom_recinto', 'zona')
    list_display = ('id', 'nom_recinto', 'zona')


@admin.register(Circun)
class CircunAdmin(admin.ModelAdmin):
    search_fields = ('id', 'nom_circunscripcion',)
    list_display = ('id', 'nom_circunscripcion', 'tipo_circun')


@admin.register(Tipo_circun)
class Tipo_circunAdmin(admin.ModelAdmin):
    search_fields = ('tipo_circun',)
    list_display = ('id', 'tipo_circun',)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ('nom_categoria', 'id')
    list_display = ('id', 'nom_categoria')


@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    search_fields = ('nom_subcategoria', 'id')
    list_display = ('id', 'nom_subcategoria', 'categoria')


