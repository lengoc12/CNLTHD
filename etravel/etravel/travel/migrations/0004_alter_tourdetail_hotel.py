# Generated by Django 3.2.7 on 2021-10-09 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0003_images_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourdetail',
            name='hotel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='travel.hotel'),
        ),
    ]