# Generated by Django 3.2.7 on 2021-09-26 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0023_alter_slider_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='name',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
