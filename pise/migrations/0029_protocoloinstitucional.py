# Generated by Django 3.2.9 on 2024-12-26 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pise', '0028_auto_20241226_1449'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProtocoloInstitucional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('SP', 'Salidas pedagógicas'), ('DE', 'Desregulación Emocional'), ('DC', 'Desregulación Conductual')], max_length=2)),
                ('version', models.CharField(max_length=10)),
                ('fecha_subida', models.DateTimeField(auto_now_add=True)),
                ('archivo', models.FileField(upload_to='protocolos/')),
                ('activo', models.BooleanField(default=True)),
                ('establecimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pise.establecimiento')),
            ],
            options={
                'verbose_name': 'Protocolo Institucional',
                'verbose_name_plural': 'Protocolos Institucionales',
                'ordering': ['-fecha_subida'],
            },
        ),
    ]