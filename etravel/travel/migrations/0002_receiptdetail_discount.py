# Generated by Django 3.2.7 on 2021-09-01 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiptdetail',
            name='discount',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='travel.discount'),
        ),
    ]
