# -*- coding: utf-8 -*-
from django.contrib import admin
from ge.models import *
from django.contrib.admin import AdminSite
import psycopg2
from mapwidgets.widgets import GooglePointFieldWidget
from django.db import connection


AdminSite.site_title = 'OEP'
AdminSite.site_header = 'OEP-Geografía Electoral'
AdminSite.index_title = 'Administración-BD'


#@admin.register(Asiento_jurisdiccion)
#class Asiento_jurisdiccion(admin.ModelAdmin):
    #pass:
    #fields = ('nom_continente',)
    #list_display = ('nom_continente', 'id')

@admin.register(Continente)
class Continente(admin.ModelAdmin):
    fields = ('nom_continente',)
    #search_fields = ('ut', 'nombre')
    list_display = ('nom_continente', 'id')


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    fields = ('id_origen', 'version', 'nom_pais', 'nom_pais_inter', 'nom_pais_alias', 'iso3166_2', 'iso3166_3', 'nacionalidad', 'periodo_ini', 'periodo_fin', 'actual', 'descripcion', 'estado', 'continente', 'fecha_ingreso', 'lat_ref', 'long_ref', 'geohash_ref')
    search_fields = ['nom_pais', 'continente']
    list_display = ('id', 'nom_pais', 'continente')


@admin.register(Ut_sup)
class Ut_supAdmin(admin.ModelAdmin):
    search_fields = ('nom_ut_sup', 'pais__nom_pais')
    list_display = ('id', 'nom_ut_sup', 'pais')


@admin.register(Ut_intermedia)
class Ut_intermediaAdmin(admin.ModelAdmin):
    search_fields = ('nom_ut_intermedia', 'ut_sup__nom_ut_sup')
    list_display = ('id', 'nom_ut_intermedia', 'ut_sup')


@admin.register(Ut_basica)
class Ut_basicaAdmin(admin.ModelAdmin):
    search_fields = ('nom_ut_basica', 'ut_intermedia__nom_ut_intermedia')
    list_display = ('id', 'nom_ut_basica', 'ut_intermedia')



def prefetch_idloc(instance):
    """ Fetch the next value in a django id autofield postgresql sequence """
    cursor = connection.cursor()
    cursor.execute(
        "SELECT last_value + increment_by from  {0}_{1}_id_seq".format(
            instance._meta.app_label.lower(),
            instance._meta.object_name.lower(),
        )
    )
    row = cursor.fetchone()
    cursor.close()
    return int(row[0])



@admin.register(Localidad)
class LocalidadAdmin(admin.ModelAdmin):
    list_per_page = 30
    #search_fields = ('nom_localidad', 'ut_basica__nom_ut_basica')
    search_fields = ('nom_localidad', )
    #list_display = ('id', 'nom_localidad', 'ut_basica', 'ut_intermedia', 'ut_sup', 'pais')
    #list_display = ('id', 'nom_localidad', 'ubicacion')
    list_display = ('id', 'nom_localidad', 'cod_ungle', 'poblacion', 'ut_basica')

    #list_select_related = ('ut_basica', 'ut_intermedia', 'ut_sup', 'pais')
    ##list_select_related = ('ubicacion',)
    list_select_related = ('ut_basica',)
    list_display_links =('id', 'nom_localidad',)
    exclude = ('fecha_act',)
    readonly_fields = ('fecha_ingreso', 'fecha_act', 'geohash')
    ordering = ('nom_localidad',)

    readonly_fields = ('fecha_ingreso', 'fecha_act', 'geohash')


    fieldsets = (
        ('Datos Ubicación Geográfica', {
            'fields': ('continente', 'pais', 'ut_sup', 'ut_intermedia', 'ut_basica',
                           ('latitud', 'longitud', 'geohash')
                      )
        }),
        ('Geometría', {'fields':('geom', )
        }),
        ('Datos de la Localidad', {'fields': ('tipo_localidad', 'cod_ungle', 'nom_localidad', 'nivel_ut',  'doc_legal',
                            ('cod_ine', 'cod_ine_shp'), ('id_origen', 'version'), ('periodo_ini', 'periodo_fin', 'actual'),
                            ('poblacion', 'viviendas', 'censo'), 'fecha_ingreso', 'fecha_act'
                            )
        }),
        #('Datos si existe Oficialía de Registro Civil', {'fields':('existe_orc', 'numero_orc')
        #}),
    )

    def save_model(self, request, obj, form, change):
        try:
            cur = connection.cursor()
            sql = """
                select st_SetSRID(st_MakePoint(%s, %s), 4326)
                """
            cur.execute(sql, (obj.longitud, obj.latitud))
            obj.geom = cur.fetchone()[0]

            sql = """
                select st_Geohash(st_SetSRID(st_MakePoint(%s, %s), 4326), 8)
                """
            #cur.execute(sql, (obj.geom))
            cur.execute(sql, (obj.longitud, obj.latitud))
            obj.geohash = cur.fetchone()[0]
            #obj.id_origen =  obj.id  #prefetch_idloc(instance)   #pend solo p new

            cur.close()

            obj.save()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


@admin.register(Nivel_ut)
class Nivel_utAdmin(admin.ModelAdmin):
    search_fields = ('ut_descripcion', 'pais')
    list_display = ('id', 'ut_descripcion', 'pais')


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    exclude = ('geom',)

# to asiento
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


#class Asiento_circunInline(admin.TabularInline):
#    model = Asiento_circun
#    extra = 1


class Asiento_imgInline(admin.TabularInline):
    model = Asiento_img


class Asiento_detalleInline(admin.TabularInline):
    model = Asiento_detalle


class Asiento_distritoInline(admin.TabularInline):
    model = Asiento_distrito
    extra = 1

@admin.register(Asiento)
class AsientoAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }

    #list_filter = ('ut_basica',)
    list_filter = ('ut_sup',)
    search_fields = ('nom_asiento', 'ut_basica')
    list_display = ('id', 'nom_asiento', 'ubicacion')
    #exclude = ('fecha_act', 'geom')
    exclude = ('fecha_act', )
    readonly_fields = ('fecha_ingreso', 'fecha_act', 'geohash')
    list_display_links =('id', 'nom_asiento',)
    date_hierarchy = 'fecha_act'
    ordering = ('nom_asiento',)
    #raw_id_fields = ('localidad',)
    #+RutaInline  inlines = (Asiento_distritoInline, Asiento_detalleInline, Asiento_imgInline, RutaInline, Asiento_jurisdiccionInline)
    inlines = (Asiento_distritoInline, Asiento_detalleInline, Asiento_imgInline, Asiento_jurisdiccionInline)

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
        ('Geometría', {'fields':('geom', )
        }),
        ('Datos del Asiento Electoral', {'fields': ('nom_asiento', 'doc_actualizacion', 'fecha_doc_actualizacion', 'estado',
                          'proceso_activo', 'etapa', 'fecha_ingreso', 'obs', 'descripcion_ubicacion', ('idloc')
                          )
        }),
        ('Datos si existe Oficialía de Registro Civil', {'fields':('existe_orc', 'numero_orc')
        }),
    )

    def save_model(self, request, obj, form, change):
        try:
            cur = connection.cursor()
            sql = """
                select st_SetSRID(st_MakePoint(%s, %s), 4326)
                """
            cur.execute(sql, (obj.longitud, obj.latitud))
            obj.geom = cur.fetchone()[0]

            sql = """
                select st_Geohash(st_SetSRID(st_MakePoint(%s, %s), 4326), 8)
                """
            #cur.execute(sql, (obj.geom))
            cur.execute(sql, (obj.longitud, obj.latitud))
            obj.geohash = cur.fetchone()[0]

            cur.close()

            obj.save()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


@admin.register(Distrito)
class DistritoAdmin(admin.ModelAdmin):
    search_fields = ('distrito', 'fecha_ingreso', 'id')
    list_display = ('id', 'distrito', 'fecha_ingreso', 'ubicacion')
    exclude = ('fecha_act',)
    readonly_fields = ('fecha_ingreso', 'fecha_act')
    list_display_links =('id', 'distrito',)

    fieldsets = (
        ('Datos Ubicación Geográfica', {
            'fields': ('pais', 'ut_sup', 'ut_basica',
                      )
        }),
        ('Datos del Distrito', {'fields': ('distrito', 'nro_distrito', 'etapa', 'fecha_ingreso', 'obs', 'geom'
                          )
        }),
    )


@admin.register(Asiento_distrito)
class Asiento_distritoAdmin(admin.ModelAdmin):
    search_fields = ('distrito', 'asiento')
    list_display = ('id', 'distrito', 'asiento')


@admin.register(Asiento_img)
class Asiento_imgAdmin(admin.ModelAdmin):
    search_fields = ('asiento', )
    list_display = ('id', 'asiento', 'vista', 'img')


@admin.register(Asiento_jurisdiccion)
class Asiento_jurisdiccion(admin.ModelAdmin):
    list_display = ('id', 'distancia_km', 'obs')


#class Zona_circunInline(admin.TabularInline):
 #   model = Asiento_circun
  #  extra = 1


@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    search_fields = ('zona', 'distrito', 'ut_basica')
    list_display = ('id', 'zona', 'fecha_ingreso', 'ubicacion')
    exclude = ('fecha_act',)
    readonly_fields = ('fecha_ingreso', 'fecha_act')
    list_display_links =('id', 'zona',)

    fieldsets = (
        ('Datos Ubicación Geográfica', {
            'fields': ('pais', 'ut_sup', 'ut_basica', 'distrito'
                    )
        }),
        ('Datos de la Zona', {'fields': ('zona', 'etapa', 'fecha_ingreso', 'obs', 'geom' )
        }),
        ('Circunscripción', {
            'fields': ('circun',
                    )
        }),
    )

# recinto

class Recinto_imgInline(admin.TabularInline):
    model = Recinto_img


class Recinto_detalleInline(admin.TabularInline):
    model = Recinto_detalle


@admin.register(Recinto)
class RecintoAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }

    list_filter = ('ut_basica',)
    search_fields = ('nom_recinto', 'ut_basica')
    list_display = ('id', 'nom_recinto', 'ubicacion')
    exclude = ('fecha_act',  )
    readonly_fields = ('fecha_ingreso', 'fecha_act', 'geohash', )
    list_display_links =('id', 'nom_recinto',)
    date_hierarchy = 'fecha_act'
    ordering = ('nom_recinto',)
    inlines = (Recinto_detalleInline, Recinto_imgInline) #, RutaInline, Asiento_jurisdiccionInline)

    fieldsets = (
        ('Datos Ubicación Geográfica', {
            'fields': ('continente', 'pais', 'ut_sup', 'ut_intermedia', 'ut_basica', 'asiento', ('asiento_distrito', 'distrito'), ('zona', 'direccion'),
                           ('latitud', 'longitud', 'geohash')
                      )
        }),
        ('Geometría', {'fields':('geom', )
        }),
        ('Datos del Recinto Electoral', {'fields': ('nom_recinto', 'estado', 'tipo', 'tipo_circun', 'doc_actualizacion', 'fecha_doc_actualizacion',
                          'max_mesas', 'nro_pisos', 'nro_aulas', ('rue', 'rue1', 'rue2'), 'etapa', 'fecha_ingreso', 'obs', ('idloc', 'reci')
                          )
        }),
    )

    def save_model(self, request, obj, form, change):
        try:
            cur = connection.cursor()
            sql = """
                select st_SetSRID(st_MakePoint(%s, %s), 4326)
                """
            cur.execute(sql, (obj.longitud, obj.latitud))
            obj.geom = cur.fetchone()[0]

            sql = """
                select st_Geohash(st_SetSRID(st_MakePoint(%s, %s), 4326), 8)
                """
            #cur.execute(sql, (obj.geom))
            cur.execute(sql, (obj.longitud, obj.latitud))
            obj.geohash = cur.fetchone()[0]

            cur.close()

            obj.save()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


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


