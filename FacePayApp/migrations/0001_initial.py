# Generated by Django 5.0.2 on 2024-03-16 05:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=50)),
                ('due_date', models.DateField()),
                ('from_name', models.CharField(max_length=100)),
                ('from_email_address', models.EmailField(max_length=254)),
                ('from_phone_number', models.CharField(max_length=15)),
                ('to_name', models.CharField(max_length=100)),
                ('to_email_address', models.EmailField(max_length=254)),
                ('to_phone_number', models.CharField(max_length=15)),
                ('discount_percentage', models.DecimalField(decimal_places=3, max_digits=5)),
                ('tax_percentage', models.DecimalField(decimal_places=3, max_digits=5)),
                ('total_cost', models.DecimalField(decimal_places=3, max_digits=5)),
                ('notes', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserInformation',
            fields=[
                ('userId', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('age', models.DateField(auto_now_add=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=3, max_digits=5)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=50)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='FacePayApp.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='FinancialInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=100)),
                ('account_number', models.CharField(max_length=50)),
                ('ifsc_code', models.CharField(max_length=12)),
                ('upi_id', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FacePayApp.userinformation')),
            ],
        ),
    ]