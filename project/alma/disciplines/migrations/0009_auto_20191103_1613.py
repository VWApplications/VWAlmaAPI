# Generated by Django 2.1.4 on 2019-11-03 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('disciplines', '0008_auto_20191103_0319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discipline',
            name='monitors',
            field=models.ManyToManyField(blank=True, related_name='monitor_classes', to='alma_accounts.AlmaUser', verbose_name='Monitores'),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='student_classes', to='alma_accounts.AlmaUser', verbose_name='Alunos'),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disciplines', to='alma_accounts.AlmaUser', verbose_name='Professor'),
        ),
    ]
