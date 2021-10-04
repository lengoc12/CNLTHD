# Generated by Django 3.2.7 on 2021-09-01 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_receiptdetail_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='id_card',
            field=models.CharField(default='', max_length=12, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='mobile_number',
            field=models.CharField(default='', max_length=10, unique=True),
        ),
    ]