# Generated by Django 4.0.5 on 2022-07-16 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_student_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='admission_number',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
