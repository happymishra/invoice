# Generated by Django 3.0 on 2019-12-27 07:46

import apps.api.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('street', models.CharField(max_length=50)),
                ('pin_code', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'address',
            },
        ),
        migrations.CreateModel(
            name='BuyerSeller',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('address_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Address')),
            ],
            options={
                'db_table': 'buyerseller',
            },
        ),
        migrations.CreateModel(
            name='InvoiceDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('invoice_number', models.CharField(max_length=20, null=True)),
                ('invoice_date', models.DateTimeField(null=True)),
                ('amount', models.FloatField(null=True)),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buyer', to='api.BuyerSeller')),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seller', to='api.BuyerSeller')),
            ],
            options={
                'db_table': 'invoicedetail',
            },
        ),
        migrations.CreateModel(
            name='UploadInvoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(default=10)),
                ('status', models.IntegerField(default=1)),
                ('creation_date', models.DateTimeField(default=datetime.datetime.now)),
                ('file_path', models.FileField(upload_to=apps.api.models.set_file_path)),
                ('invoice_detail', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.InvoiceDetail')),
            ],
            options={
                'db_table': 'uploadinvoice',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('item', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('invoice_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.InvoiceDetail')),
            ],
            options={
                'db_table': 'item',
            },
        ),
    ]