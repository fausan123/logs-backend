# Generated by Django 4.0.5 on 2022-07-16 15:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_student_admission_number'),
        ('subjects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to='subjects.subject')),
            ],
        ),
        migrations.CreateModel(
            name='AssessmentQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='subjects.assessment')),
                ('learningoutcomes', models.ManyToManyField(related_name='questions', to='subjects.learningoutcome')),
            ],
        ),
        migrations.CreateModel(
            name='AssessmentSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='subjects.assessment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='users.student')),
            ],
            options={
                'unique_together': {('student', 'assessment')},
            },
        ),
        migrations.CreateModel(
            name='QAGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qagrades', to='subjects.assessmentquestion')),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qagrades', to='subjects.assessmentsubmission')),
            ],
            options={
                'unique_together': {('submission', 'question')},
            },
        ),
    ]
