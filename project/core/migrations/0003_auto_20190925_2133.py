# Generated by Django 2.1.4 on 2019-09-26 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190921_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='tags',
            field=models.ManyToManyField(null=True, related_name='tags', related_query_name='news', to='core.Tag'),
        ),
    ]