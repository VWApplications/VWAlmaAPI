# Generated by Django 2.1.4 on 2019-11-03 06:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AlmaUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Data na qual o objeto foi criado.', verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Data na qual o objeto foi atualizado.', verbose_name='Atualizado em')),
                ('identifier', models.CharField(blank=True, help_text='Identificador dentro de sua universidade', max_length=50, verbose_name='Mátricula')),
                ('photo', models.ImageField(blank=True, help_text='Foto do usuário', null=True, upload_to='accounts')),
                ('permission', models.CharField(default='STUDENT', help_text='Verifica o tipo de permissão que o usuário tem.', max_length=50, verbose_name='Permissão.')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='alma', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'alma_user',
            },
        ),
    ]
