# Generated by Django 4.0.5 on 2022-07-14 19:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_alter_user_is_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='users.faculty')),
                ('students', models.ManyToManyField(related_name='subjects', to='users.student')),
            ],
        ),
        migrations.CreateModel(
            name='LearningOutcome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learningoutcomes', to='subjects.subject')),
            ],
        ),
    ]
