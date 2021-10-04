# Generated by Django 3.2.7 on 2021-09-02 16:58

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0009_remove_receiptdetail_discount'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='tourdetail',
            name='transports',
            field=models.ManyToManyField(blank=True, null=True, related_name='tours', to='travel.Transport'),
        ),
    ]