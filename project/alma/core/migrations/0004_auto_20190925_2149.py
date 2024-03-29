# Generated by Django 2.1.4 on 2019-09-26 00:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190925_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Date that the object is updated.', verbose_name='Updated at'),
        ),
        migrations.AddField(
            model_name='tag',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Date that the object is created.', verbose_name='Created at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Date that the object is updated.', verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='news',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Date that the object is created.', verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='news',
            name='tags',
            field=models.ManyToManyField(null=True, related_name='news', to='core.Tag'),
        ),
    ]
