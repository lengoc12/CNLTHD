# Generated by Django 3.2.7 on 2021-09-02 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0008_alter_tour_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receiptdetail',
            name='discount',
        ),
    ]
