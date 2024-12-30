# Generated by Django 3.2.9 on 2022-08-09 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pise', '0018_alter_establecimiento_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matricula',
            name='alumno',
        ),
        migrations.AddField(
            model_name='matricula',
            name='Comuna_residencia',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='matricula',
            name='apellido_materno',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='matricula',
            name='apellido_paterno',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='matricula',
            name='celular',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='matricula',
            name='codigo_etnia',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='matricula',
            name='domicilio_actual',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='matricula',
            name='dv',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='matricula',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='matricula',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='matricula',
            name='nombre_apoderado',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='matricula',
            name='nombres',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='matricula',
            name='rut',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='matricula',
            name='telefono',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='Alumno',
        ),
    ]