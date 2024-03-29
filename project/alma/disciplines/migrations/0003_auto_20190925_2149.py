# Generated by Django 2.1.4 on 2019-09-26 00:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('disciplines', '0002_auto_20190921_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discipline',
            name='classroom',
            field=models.CharField(help_text='Classroom title of discipline.', max_length=10, verbose_name='Classroom'),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='course',
            field=models.CharField(blank=True, help_text='Course that is ministered the discipline', max_length=100, verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Date that the object is created.', verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='institution',
            field=models.CharField(blank=True, help_text='University or School in which the user is inserted.', max_length=100, verbose_name='Institution'),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disciplines', to=settings.AUTH_USER_MODEL, verbose_name='Teacher'),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Date that the object is updated.', verbose_name='Updated at'),
        ),
    ]
