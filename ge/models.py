# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.gis.db import models
from model_utils import Choices


class Continente (models.Model):
    nom_continente = models.CharField(max_length=100,
            verbose_name='Nombre del Continente')
    geom = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'g_continente'

    def __unicode__(self):
        return self.nom_continente


class Pais(models.Model):
    id_origen = models.IntegerField()
    version = models.PositiveSmallIntegerField()
    nom_pais = models.CharField(max_length=100,
            help_text='Nombre del país',
            verbose_name='Nombre del país')
    nom_pais_inter = models.CharField(max_length=100,
            help_text='Nombre del país internacional')
    nom_pais_alias = models.CharField(max_length=100,
            help_text='Nombre corto del país')
    iso3166_2 = models.CharField(max_length=2,
            help_text='Código de 2 caracteres de acuerdo al ISO3166')
    iso3166_3 = models.CharField(max_length=3,
            help_text='Código de 3 caracteres de acuerdo al ISO3166')
    nacionalidad = models.CharField(max_length=50,
            help_text='Descripción genérica de la nacionalidad')
    periodo_ini = models.DateField(
            help_text='Periodo inicial de vigencia del registro país')
    periodo_fin = models.DateField(
            help_text='Periodo final de vigencia del registro país')
    actual = models.BooleanField(
            help_text='Especifica el estado activo o dado de baja lógica')
    descripcion = models.TextField(blank=True,
            help_text='Descripción del motivo de creación y/o actualización')
    estado =  models.BooleanField(
            help_text='True si el país participa en procesos electorales')
    continente = models.ForeignKey('Continente')
    fecha_ingreso = models.DateField(
            help_text='Fecha de ingreso al sistema')
    lat_ref = models.FloatField(
            help_text='Latitud del lugar de referencia del país (Capital)')
    geom = models.MultiPolygonField()
    long_ref = models.FloatField(
            help_text='Longitud del lugar de referencia del país (Capital)')
    geohash_ref = models.CharField(max_length=8,
            help_text='Geohash del lugar de referencia del país (Capital)')
    geom = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'g_pais'
        unique_together = ('id_origen', 'version')

    def __unicode__(self):
        return self.nom_pais

    def nacionalidad_show(self):
        return self.nacionalidad


class Nivel_ut(models.Model):
    ut_descripcion = models.CharField(max_length=100,
            help_text='Descripción de la unidad territorial según país')
    pais = models.ForeignKey('Pais')
    jerarquia = models.PositiveSmallIntegerField(null=True,
            verbose_name = 'Jerarquía',
            help_text='Jerarquía de la Unidad Territorial de acuerdo al País')

    class Meta:
        db_table = 'g_nivel_ut'
        unique_together = ('id', 'jerarquia')

    def __unicode__(self):
        return self.ut_descripcion

class Ut_sup(models.Model):
    id_origen = models.IntegerField()
    version = models.PositiveSmallIntegerField()
    nivel_ut = models.ForeignKey('Nivel_ut')
    nom_ut_sup = models.CharField(max_length=80,
            verbose_name = 'Nombre Ud.Terr. Superior')
    pais = models.ForeignKey('Pais')
    cod_ine = models.CharField(max_length=2,
            help_text='Código del INE si corresponde a Bolivia',
            verbose_name = 'Código INE')
    periodo_ini = models.DateField(
            help_text='Periodo inicial de vigencia de la unidad territorial')
    periodo_fin = models.DateField(
            help_text='Periodo final de vigencia de la unidad territorial')
    actual = models.BooleanField(
            help_text='Indica si la unidad territorial esta vigente')
    doc_legal = models.CharField(max_length=100,
            help_text='Indica si la unidad territorial esta vigente')
    fecha_ingreso = models.DateField(
            help_text='Fecha de ingreso al sistema')
    lat_ref = models.FloatField(
            help_text='Latitud del lugar de referencia')
    long_ref = models.FloatField(
            help_text='Longitud del lugar de referencia')
    geohash_ref = models.CharField(max_length=7,
            help_text='Geohash del lugar de referencia')
    geom = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'g_ut_sup'
        unique_together = ('id_origen', 'version')

    def __unicode__(self):
        return self.nom_ut_sup


class Ut_intermedia(models.Model):
    id_origen = models.IntegerField()
    version = models.PositiveSmallIntegerField()
    nivel_ut = models.ForeignKey('Nivel_ut')
    nom_ut_intermedia = models.CharField(max_length=80,
            verbose_name = 'Nombre Ud.Terr. Intermedia')
    cod_ine = models.CharField(max_length=4,
            help_text='Código del INE si corresponde a Bolivia',
            verbose_name = 'Código INE')
    periodo_ini = models.DateField(
            help_text='Periodo inicial de vigencia de la unidad territorial')
    periodo_fin = models.DateField(
            help_text='Periodo final de vigencia de la unidad territorial')
    actual = models.BooleanField(
            help_text='Indica si la unidad territorial esta vigente')
    doc_legal = models.CharField(max_length=100,
            help_text='Indica si la unidad territorial esta vigente')
    ut_sup = models.ForeignKey('Ut_sup')
    ut_intermedia_id = models.IntegerField(
            help_text='Será utilizado para definir más niveles a futuro de ser necesario - recursivo')
    fecha_ingreso = models.DateField(
            help_text='Fecha de ingreso al sistema')
    lat_ref = models.FloatField(
            help_text='Latitud del lugar de referencia')
    long_ref = models.FloatField(
            help_text='Longitud del lugar de referencia')
    geohash_ref = models.CharField(max_length=7,
            help_text='Geohash del lugar de referencia')
    geom = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'g_ut_intermedia'
        unique_together = ('id_origen', 'version')

    def __unicode__(self):
        return self.nom_ut_intermedia

class Ut_basica(models.Model):
    id_origen = models.IntegerField()
    version = models.PositiveSmallIntegerField()
    nivel_ut = models.ForeignKey('Nivel_ut')
    nom_ut_basica = models.CharField(max_length=80,
            verbose_name = 'Nombre Ud.Terr. Básica')
    cod_ine = models.CharField(max_length=6,
            help_text='Código del INE si corresponde a Bolivia',
            verbose_name = 'Código INE')
    periodo_ini = models.DateField(
            help_text='Periodo inicial de vigencia de la unidad territorial')
    periodo_fin = models.DateField(
            help_text='Periodo final de vigencia de la unidad territorial')
    actual = models.BooleanField(
            help_text='Indica si la unidad territorial esta vigente')
    doc_legal = models.CharField(max_length=100,
            help_text='Indica si la unidad territorial esta vigente')
    ut_intermedia = models.ForeignKey('Ut_intermedia')
    fecha_ingreso = models.DateField(
            help_text='Fecha de ingreso al sistema')
    lat_ref = models.FloatField(
            help_text='Latitud del lugar de referencia')
    long_ref = models.FloatField(
            help_text='Longitud del lugar de referencia')
    geohash_ref = models.CharField(max_length=7,
            help_text='Geohash del lugar de referencia')
    geom = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'g_ut_basica'
        unique_together = ('id_origen', 'version')

    def __unicode__(self):
        return self.nom_ut_basica


class Localidad(models.Model):
    id_origen = models.IntegerField()
    version = models.PositiveSmallIntegerField()
    nivel_ut = models.ForeignKey('Nivel_ut')
    nom_localidad = models.CharField(max_length=80,
            verbose_name = 'Nombre Ud.Terr. - equivalente a localidad en Bolivia')
    cod_ine = models.CharField(max_length=6,
            help_text='Código del INE si corresponde a Bolivia',
            verbose_name = 'Código INE')
    cod_ine_shp = models.CharField(max_length=15,
            help_text='Código del INE de fuente shapefile',
            verbose_name = 'Código INE - shapefile')
    periodo_ini = models.DateField(
            help_text='Periodo inicial de vigencia de la unidad territorial')
    periodo_fin = models.DateField(
            help_text='Periodo final de vigencia de la unidad territorial')
    actual = models.BooleanField(
            help_text='Indica si la unidad territorial esta vigente')
    censo = models.IntegerField(
            help_text='Año del Censo realizado por el INE')
    poblacion = models.IntegerField(
            help_text='Número de Población según el censo')
    viviendas = models.IntegerField(
            help_text='Número de viviendas según el censo')
    doc_legal = models.CharField(max_length=100,
            help_text='Indica si la unidad territorial esta vigente')
    ut_basica = models.ForeignKey('Ut_basica')
    fecha_ingreso = models.DateField(
            help_text='Fecha de ingreso al sistema')
    latitud = models.FloatField(
            help_text='Latitud de la Localidad')
    longitud = models.FloatField(
            help_text='Longitud de la localidad')
    geohash = models.CharField(max_length=7,
            help_text='Geohash de la ubicación de la Localidad')
    geom = models.PointField(null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'g_localidad'
        unique_together = ('id_origen', 'version')

    def __unicode__(self):
        return self.nom_localidad


class Localidad_fuente(models.Model):
    localidad = models.ForeignKey('Localidad')
    nom_localidad = models.CharField(max_length=80)
    censo = models.IntegerField()
    poblacion = models.IntegerField()
    viviendas = models.IntegerField()
    geom = models.PointField(null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'g_localidad_fuente'

    def __unicode__(self):
        return self.nom_localidad

## ge
class Asiento(models.Model):
    ESTADOS = Choices(
        (1, 'ACTIVO', ('ACTIVO')),
        (2, 'REHABILITADO', ('REHABILITADO')),
        (3, 'TRASLADADO', ('TRASLADADO')),
        (4, 'SUSPENDIDO', ('SUSPENDIDO')),
        (5, 'SUPRIMIDO', ('SUPRIMIDO')))
    ETAPAS = Choices(
        (1, 'PROPUESTA', ('PROPUESTA')),
        (2, 'REVISION', ('REVISION')),
        (3, 'APROBADO', ('APROBADO')))
    nom_asiento = models.CharField(max_length=100)
    ut_basica = models.ForeignKey('Ut_basica')
    localidad = models.ForeignKey('Localidad')
    resol_creacion = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField()
    descripcion_ubicacion = models.CharField(max_length=254)
    estado = models.PositiveSmallIntegerField(choices=ESTADOS, default=ESTADOS.ACTIVO)
    proceso_activo = models.BooleanField()
    etapa = models.PositiveSmallIntegerField(choices=ETAPAS, default=ETAPAS.PROPUESTA)
    fecha_ingreso = models.DateTimeField()
    obs = models.CharField(max_length=100)
    fecha_act = models.DateTimeField()
    latitud = models.FloatField()
    longitud = models.FloatField()
    geohash = models.CharField(max_length=8)
    geom = models.PointField(null=True)
    objects = models.GeoManager()
    # GeoDjango-specific: a geometry field (MultiMultiPolygonField), and
    # overriding the default manager with a GeoManager instance.

    # Returns the string representation of the model.


    def __unicode__(self):              # __unicode__ on Python 2
        return self.nom_asiento


class Ruta(models.Model):
    nro_ruta = models.IntegerField()
    asiento = models.ForeignKey('Asiento')
    nro_tramo = models.IntegerField()
    inicio = models.CharField(max_length=80)
    fin = models.CharField(max_length=80)
    tipo = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=100)
    distancia_km = models.FloatField()
    tiempo_hrs = models.IntegerField()
    tiempo_min = models.IntegerField()
    costo = models.FloatField()
    obs = models.CharField(max_length=100)
    fecha_act = models.DateTimeField()
    geom = models.LineStringField(null=True)
    objects = models.GeoManager()


class Asiento_jurisdiccion(models.Model):
    asiento = models.ForeignKey('Asiento')
    localidad = models.ForeignKey('Localidad')
    accesibilidad = models.CharField(max_length=100)
    distancia_km = models.FloatField()
    geohash = models.CharField(max_length=8)
    latitud = models.FloatField()
    longitud = models.FloatField()
    obs = models.CharField(max_length=100)
    fecha_act = models.DateTimeField()
    geom = models.PointField(null=True)
    objects = models.GeoManager()


class Asiento_img(models.Model):
    VISTAS = Choices(
        (1, 'PANORAMICA', ('PANORAMICA')),
        (2, 'VISTA1', ('VISTA1')),
        (3, 'VISTA2', ('VISTA2')),
        (4, 'VISTA3', ('VISTA3')))
    asiento = models.ForeignKey('Asiento')
    vista = models.PositiveSmallIntegerField(choices=VISTAS)
    img = models.ImageField(upload_to="img", null=True, blank=True)

    class Meta:
        unique_together = ('asiento', 'vista')


class Tipo_circun(models.Model):
    tipo_circun = models.CharField(max_length=40)

    def __unicode__(self):
        return self.tipo_circun

class Circun(models.Model):
    circun = models.PositiveSmallIntegerField()
    nom_circunscripcion = models.CharField(max_length=100)
    tipo_circun = models.ForeignKey('Tipo_circun')
    asientos = models.ManyToManyField('Asiento', through='asiento_circun')
    geom = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.nom_circunscripcion
    class Admin:
        pass


class Asiento_circun(models.Model):
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE)
    circun = models.ForeignKey(Circun, on_delete=models.CASCADE)


class Distrito(models.Model):
    ETAPAS = Choices(
        (1, 'PROPUESTA', ('PROPUESTA')),
        (2, 'REVISION', ('REVISION')),
        (3, 'APROBADO', ('APROBADO')))
    asientos = models.ManyToManyField('Asiento', through='asiento_distrito')
    distrito = models.CharField(max_length=100)
    etapa = models.PositiveSmallIntegerField(choices=ETAPAS, default=ETAPAS.PROPUESTA)
    fecha_ingreso = models.DateTimeField()
    obs = models.CharField(max_length=150)
    fecha_act = models.DateTimeField()
    geom = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.distrito


class Asiento_distrito(models.Model):
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE)


class Zona(models.Model):
    ETAPAS = Choices(
        (1, 'PROPUESTA', ('PROPUESTA')),
        (2, 'REVISION', ('REVISION')),
        (3, 'APROBADO', ('APROBADO')))
    zona = models.CharField(max_length=100)
    distrito = models.ForeignKey('Distrito')
    etapa = models.PositiveSmallIntegerField(choices=ETAPAS, default=ETAPAS.PROPUESTA)
    fecha_ingreso = models.DateTimeField()
    obs = models.CharField(max_length=120)
    fecha_act = models.DateTimeField()
    lat_ref = models.FloatField(
            help_text='Latitud del lugar de referencia')
    long_ref = models.FloatField(
            help_text='Longitud del lugar de referencia')
    geohash_ref = models.CharField(max_length=7,
            help_text='Geohash del lugar de referencia')
    geom = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.zona


class Recinto(models.Model):
    ESTADOS = Choices(
        (1, 'ACTIVO', ('ACTIVO')),
        (2, 'REHABILITADO', ('REHABILITADO')),
        (3, 'TRASLADADO', ('TRASLADADO')),
        (4, 'SUSPENDIDO', ('SUSPENDIDO')),
        (5, 'SUPRIMIDO', ('SUPRIMIDO')))
    ETAPAS = Choices(
        (1, 'PROPUESTA', ('PROPUESTA')),
        (2, 'REVISION', ('REVISION')),
        (3, 'APROBADO', ('APROBADO')))
    tipo = models.PositiveSmallIntegerField()
    zona = models.ForeignKey('Zona')
    nom_recinto = models.CharField(max_length=100)
    max_mesas = models.PositiveSmallIntegerField()
    cantidad_pisos = models.PositiveIntegerField()
    direccion = models.CharField(max_length=150)
    estado = models.PositiveSmallIntegerField(
        choices=ESTADOS, default=ESTADOS.ACTIVO)
    tipo_circun = models.ForeignKey('Tipo_circun')
    rue = models.PositiveIntegerField()
    etapa = models.PositiveSmallIntegerField(choices=ETAPAS, default=ETAPAS.PROPUESTA)
    fecha_ingreso = models.DateTimeField()
    fecha_act = models.DateTimeField()
    obs = models.CharField(max_length=120)
    latitud = models.FloatField()
    longitud = models.FloatField()
    geohash = models.CharField(max_length=9)
    geom = models.PointField(null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.nom_recinto

class Recinto_img(models.Model):
    VISTAS = Choices(
        (1, 'FRONTAL', ('FRONTAL')),
        (2, 'INTERIOR', ('INTERIOR')),
        (3, 'LATERAL_IZQ', ('LATERAL_IZQ')),
        (4, 'LATERAL_DER', ('LATERAL_DER')))
    recinto = models.ForeignKey('Recinto')
    vista = models.PositiveSmallIntegerField(choices=VISTAS)
    img = models.ImageField(upload_to="img", null=True, blank=True)

    class Meta:
        unique_together = ('recinto', 'vista')


class Categoria(models.Model):
    nom_categoria = models.CharField(max_length=100)

class Subcategoria(models.Model):
    categoria = models.ForeignKey('Categoria')
    nom_subcategoria = models.CharField(max_length=100)

class Recinto_detalle(models.Model):
    recinto = models.ForeignKey('Recinto')
    subcategoria = models.ForeignKey('Subcategoria')
    descripcion = models.CharField(max_length=100)


class Asiento_detalle(models.Model):
    asiento = models.ForeignKey('Asiento')
    subcategoria = models.ForeignKey('Subcategoria')
    descripcion = models.CharField(max_length=100)

