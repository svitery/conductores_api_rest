# Generated by Django 3.2.5 on 2021-07-24 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datos', '0006_alter_pedidos_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidos',
            name='time',
            field=models.CharField(max_length=13, primary_key=True, serialize=False),
        ),
    ]
