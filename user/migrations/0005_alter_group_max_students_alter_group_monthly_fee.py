# Generated by Django 5.2.4 on 2025-07-10 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_group_max_students_group_monthly_fee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='max_students',
            field=models.PositiveSmallIntegerField(default=15, help_text='Maximum number of students in a group'),
        ),
        migrations.AlterField(
            model_name='group',
            name='monthly_fee',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
