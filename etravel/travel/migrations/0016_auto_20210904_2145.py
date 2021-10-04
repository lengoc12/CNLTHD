# Generated by Django 3.2.7 on 2021-09-04 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0015_alter_blog_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(default=None, upload_to='images/blog/%Y/%m'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='image',
            field=models.ImageField(default=None, upload_to='images/tour/%Y/%m'),
        ),
    ]