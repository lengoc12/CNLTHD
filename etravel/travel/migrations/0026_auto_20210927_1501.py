# Generated by Django 3.2.7 on 2021-09-27 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0025_destination_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='discount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tour',
            name='oldprice',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tour',
            name='price',
            field=models.PositiveIntegerField(),
        ),
        migrations.DeleteModel(
            name='Discount',
        ),
    ]
