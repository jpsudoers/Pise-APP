# Generated by Django 3.2.9 on 2024-12-27 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pise', '0030_auto_20241227_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maltrato',
            name='victima',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pise.matricula'),
        ),
    ]
