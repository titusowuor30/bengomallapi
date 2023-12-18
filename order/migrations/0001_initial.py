# Generated by Django 4.2.6 on 2023-12-18 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stockinventory', '0001_initial'),
        ('human_resource', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(default='36477481', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('payment_status', models.CharField(default='pending', max_length=50)),
                ('confirm_status', models.CharField(default='pending', max_length=50)),
                ('dispatch_status', models.CharField(default='pending', max_length=50)),
                ('delivery_from_date', models.DateTimeField(blank=True, null=True)),
                ('delivery_to_date', models.DateTimeField(blank=True, null=True)),
                ('delivered_status', models.CharField(default='pending', max_length=100)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='human_resource.customer')),
                ('delivery_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='human_resource.pickupstations')),
            ],
            options={
                'verbose_name_plural': 'Order',
                'db_table': 'order',
                'ordering': ['-created_at'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('retail_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quantity', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitems', to='order.order')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitems', to='stockinventory.stockinventory')),
            ],
            options={
                'verbose_name_plural': 'Order Items',
                'db_table': 'orderitems',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_id', models.CharField(default='36477481', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('status', models.CharField(default='pending', max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='human_resource.customer')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='order.order')),
            ],
            options={
                'verbose_name_plural': 'Invoices',
                'db_table': 'invoices',
                'ordering': ['-created_at'],
                'managed': True,
            },
        ),
    ]