# Generated by Django 3.2.7 on 2021-09-27 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0026_auto_20210927_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='oldprice',
        ),
        migrations.AlterField(
            model_name='tour',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_value', models.IntegerField(default=0)),
                ('create_date', models.DateTimeField()),
                ('valid_until', models.DateTimeField()),
                ('tour', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='travel.tour')),
            ],
        ),
    ]