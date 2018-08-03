from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ge.models import Recinto, Asiento
from django.db import connection

@receiver(post_save, sender=Recinto)
def model_post_save(sender, **kwargs):
    if kwargs.get('created', False):
        action_is= 'new'
    else:
        action_is= 'update'

    c1 = connection.cursor()
    c1.callproc('f_recinto', [kwargs['instance'].id])
    r1 = c1.fetchone()

    c2 = connection.cursor()
    c2.callproc('f_user', [kwargs['instance'].id])
    r2 = c2.fetchone()

    print(action_is)

    if action_is=='new':
        sql = """insert into sde._recintos (
            id, recinto, direccion, max_mesas, nro_pisos,
            nro_aulas, tipo, asiento, zona, municipio,
            provincia, departamento, estado, tipo_circun, circunscripcion,
            fecha_ingreso, fecha_act, idloc, reci, latitud,
            longitud, geom, username, event, datetime)
            values
            (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
            )"""
        c1.execute (sql, (
            r1[0], r1[1], r1[2], r1[3], r1[4],
            r1[5], r1[6], r1[7], r1[8], r1[9],
            r1[10], r1[11], r1[12], r1[13], r1[14],
            r1[15], r1[16], r1[17], r1[18], r1[19],
            r1[20], r1[21], r2[0], r2[1], r2[2]
            ))

    else:
        sql= """
            update sde._recintos set
                recinto= %s, direccion= %s, max_mesas= %s, nro_pisos= %s,
                nro_aulas= %s, tipo= %s, asiento= %s, zona= %s, municipio= %s,
                provincia= %s, departamento= %s, estado= %s, tipo_circun= %s, circunscripcion= %s,
                fecha_ingreso= %s, fecha_act= %s, idloc= %s, reci= %s, latitud= %s,
                longitud= %s, geom= %s, username= %s, event= %s, datetime= %s
            where id = %s
            """
        c1.execute (sql, (
            r1[1], r1[2], r1[3], r1[4],
            r1[5], r1[6], r1[7], r1[8], r1[9],
            r1[10], r1[11], r1[12], r1[13], r1[14],
            r1[15], r1[16], r1[17], r1[18], r1[19],
            r1[20], r1[21], r2[0], r2[1], r2[2],
            r1[0]
            ))

    c1.close
    c2.close


@receiver(post_delete, sender=Recinto)
def model_post_delete(sender, **kwargs):
    print('******************************************')
    print ("DELETED: %s" % str(kwargs['instance'].id) + '---' +  kwargs['instance'].nom_recinto)
    print('******************************************')
    with connection.cursor() as cursor:
        try:
            sql = "delete from sde._recintos where id = %s;"
            cursor.execute (sql, (int(kwargs['instance'].id),))
        except Exception as e:
            print(type(e))
            print(e.args)
            print(e)