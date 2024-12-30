# Generated by Django 3.2.9 on 2021-11-12 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pise', '0009_auto_20211105_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionarioestablecimiento',
            name='direccion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='funcionarioestablecimiento',
            name='fecha_nacionamiento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='maltrato',
            name='alumno_agresor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alumno_agresor', to='pise.matricula'),
        ),
        migrations.AddField(
            model_name='maltrato',
            name='funcionario_agresor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='funcionario_agresor', to='pise.funcionarioestablecimiento'),
        ),
        migrations.AddField(
            model_name='maltrato',
            name='funcionario_victima',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='funcionario_victima', to='pise.funcionarioestablecimiento'),
        ),
    ]