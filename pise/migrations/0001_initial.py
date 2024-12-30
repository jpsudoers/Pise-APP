# Generated by Django 3.2.8 on 2021-10-20 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.IntegerField()),
                ('dv', models.CharField(blank=True, max_length=1, null=True)),
                ('nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('apellido', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('nombre_apoderado', models.CharField(blank=True, max_length=255, null=True)),
                ('domicilio_actual', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CasoVulneracion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateField()),
                ('estado', models.CharField(choices=[('nol', 'No leido'), ('ong', 'En revisión'), ('fin', 'Finalizado')], default='nol', max_length=255)),
            ],
            options={
                'verbose_name': 'Caso Vulneracion',
                'verbose_name_plural': 'Casos vulneraciones',
                'db_table': 'caso_vulneracion',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Discriminacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_discrim', models.CharField(choices=[('cfp', 'Características físicas y/o personales'), ('ddi', 'Discapacidad física y/o intelectual'), ('em', 'Embarazo y Maternidad'), ('ig', 'Identidad de género'), ('opc', 'Opción religiosa'), ('os', 'Orientación Sexual'), ('ps', 'Problemas de Salud'), ('mr', 'Ser migrante u origen racial'), ('sda', 'Síndrome de déficit atencional')], default='cfp', max_length=255)),
                ('detalle', models.CharField(max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'discriminacion',
                'verbose_name_plural': 'discriminaciones',
                'db_table': 'discriminacion',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Establecimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('rbd', models.CharField(blank=True, max_length=6, null=True)),
                ('numero_telefonido', models.IntegerField(blank=True, null=True)),
                ('direccion', models.CharField(blank=True, max_length=255, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logo_colegio/')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MedidasDiscriminacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condicionalidad', models.BooleanField()),
                ('devolucion_casa', models.BooleanField()),
                ('expulsion', models.BooleanField()),
                ('suspension_clases', models.BooleanField()),
                ('descripcion_de_medidas', models.CharField(max_length=255)),
                ('caso', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pise.discriminacion', verbose_name='Caso Discriminacion')),
            ],
            options={
                'verbose_name': 'medida discriminacion',
                'verbose_name_plural': 'medidas discriminacion',
                'db_table': 'medidas',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel', models.CharField(blank=True, max_length=255, null=True)),
                ('letra', models.CharField(blank=True, max_length=6, null=True)),
                ('esta_activo', models.BooleanField()),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pise.alumno')),
                ('establecimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pise.establecimiento')),
            ],
        ),
        migrations.CreateModel(
            name='Maltrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateField()),
                ('estado', models.CharField(choices=[('nol', 'No leido'), ('ong', 'En revisión'), ('fin', 'Finalizado')], default='nol', max_length=255)),
                ('tipo_maltrato', models.CharField(choices=[('Estudiantes', (('adulto', 'Adulto a Estudiantes'), ('estudiante', 'Estudiante a Estudiante'))), ('Funcionarios', (('alumno_docente', 'Alumno a Docente o Funcionarios'), ('apoderado', 'Apoderado a Docente o Funcionarios')))], default='Estudiantes', max_length=255, null=True)),
                ('detalle', models.CharField(max_length=255)),
                ('victima', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pise.matricula')),
            ],
            options={
                'verbose_name': 'Caso Vulneracion Maltrato',
                'verbose_name_plural': 'Casos vulneraciones Maltrato',
                'db_table': 'caso_vulneracion_maltrato',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='discriminacion',
            name='agresor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agresor', to='pise.matricula'),
        ),
        migrations.AddField(
            model_name='discriminacion',
            name='caso',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pise.casovulneracion'),
        ),
        migrations.AddField(
            model_name='discriminacion',
            name='victima',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='victima', to='pise.matricula'),
        ),
        migrations.CreateModel(
            name='ConnotacionSexual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('nol', 'No leido'), ('ong', 'En revisión'), ('fin', 'Finalizado')], default='nol', max_length=255)),
                ('tipo_connotacion_sexual', models.CharField(choices=[('agresion', 'Agresión sexual'), ('noagresion', 'Delito de connotación sexual que no constituye agresión')], default='agresion', max_length=255)),
                ('detalle', models.CharField(max_length=255, null=True)),
                ('victima', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pise.matricula')),
            ],
        ),
        migrations.CreateModel(
            name='CasoFaltaAConvivencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('nol', 'No leido'), ('ong', 'En revision'), ('fin', 'Finalizado')], default='nol', max_length=255)),
                ('fecha_ingreso', models.DateField()),
                ('informe_detalle', models.TextField(blank=True, null=True)),
                ('matricula', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pise.matricula')),
            ],
        ),
    ]