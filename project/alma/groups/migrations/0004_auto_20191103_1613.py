# Generated by Django 2.1.4 on 2019-11-03 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_auto_20191103_0319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='student_groups', to='alma_accounts.AlmaUser', verbose_name='Students'),
        ),
    ]
