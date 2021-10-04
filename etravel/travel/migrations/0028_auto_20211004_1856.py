# Generated by Django 3.2.7 on 2021-10-04 11:56

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0027_auto_20210927_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='receiptdetail',
            name='receipt',
        ),
        migrations.RemoveField(
            model_name='receiptdetail',
            name='tour',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='name',
        ),
        migrations.AddField(
            model_name='receipt',
            name='adult',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='receipt',
            name='children',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='receipt',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Booking processing', 'Booking processing'), ('Booking accepted', 'Booking accepted'), ('Booking canceled', 'Booking canceled')], default='New', max_length=25),
        ),
        migrations.AddField(
            model_name='receipt',
            name='tour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='travel.tour'),
        ),
        migrations.AddField(
            model_name='tour',
            name='discount',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Discount',
        ),
        migrations.DeleteModel(
            name='ReceiptDetail',
        ),
    ]
