# Generated by Django 2.1.4 on 2019-09-30 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='identifier',
            field=models.CharField(blank=True, help_text='Identificador dentro de sua universidade', max_length=50, verbose_name='Mátricula'),
        ),
    ]
