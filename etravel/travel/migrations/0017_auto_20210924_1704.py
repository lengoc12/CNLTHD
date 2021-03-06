# Generated by Django 3.2.7 on 2021-09-24 10:04

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0016_auto_20210904_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
        migrations.AlterField(
            model_name='tourdetail',
            name='transports',
            field=models.ManyToManyField(blank=True, null=True, related_name='detail', to='travel.Transport'),
        ),
    ]
