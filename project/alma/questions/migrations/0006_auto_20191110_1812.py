# Generated by Django 2.1.4 on 2019-11-10 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_question_question_exam'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question_type',
            new_name='type',
        ),
        migrations.RemoveField(
            model_name='question',
            name='is_exercise',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_exam',
        ),
        migrations.AddField(
            model_name='question',
            name='exam',
            field=models.CharField(choices=[('EXERCISE', 'EXERCISE'), ('TRADITIONAL', 'TRADITIONAL'), ('TBL', 'TBL')], default='EXERCISE', help_text='Caso não for um exercício, verificar o tipo de exame ele faz parte.', max_length=30, verbose_name='Tipo de exame'),
        ),
    ]