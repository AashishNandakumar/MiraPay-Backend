# Generated by Django 5.0.2 on 2024-03-16 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FacePayApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='discount_percentage',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='tax_percentage',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_cost',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.FloatField(),
        ),
    ]
