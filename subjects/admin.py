from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.safestring import mark_safe  


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created_on", "created_by", )
    list_filter = ("created_on", "created_by", )
    search_fields = ("name__startswith", )
    ordering = ("-created_on", )

@admin.register(LearningOutcome)
class LearningOutcomeAdmin(admin.ModelAdmin):
    list_display = ("name", "subject_link", "created_on", )
    list_filter = ("created_on", "subject", )

    def subject_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:subjects_subject_change", args=(obj.subject.pk,)),
            obj.subject
        ))
    subject_link.short_description = "Subject"


    search_fields = ("name__startswith", )
    ordering = ("-created_on", )

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("title", "subject_link", "created_on", "questions_count", "submissions_count", )
    list_filter = ("created_on", "subject", )

    def subject_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:subjects_subject_change", args=(obj.subject.pk,)),
            obj.subject
        ))
    subject_link.short_description = "Subject"

    def questions_count(self, obj):
        return obj.questions.count()
    questions_count.short_description = "Questions Count"

    def submissions_count(self, obj):
        return obj.submissions.count()
    submissions_count.short_description = "Submissions Count"

    search_fields = ("title__startswith", )
    ordering = ("-created_on", )

@admin.register(AssessmentQuestion)
class AssessmentQuestionAdmin(admin.ModelAdmin):
    list_display = ("question", "assessment_link", "learningoutcomes_count", )
    list_filter = ("assessment", )

    def assessment_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:subjects_assessment_change", args=(obj.assessment.pk,)),
            obj.assessment
        ))
    assessment_link.short_description = "Assessment"

    def learningoutcomes_count(self, obj):
        return obj.learningoutcomes.count()
    learningoutcomes_count.short_description = "LO Count"

    search_fields = ("question__startswith", )

@admin.register(AssessmentSubmission)
class AssessmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "student_link", "assessment_link", "submitted_on", )
    list_filter = ("submitted_on", "assessment", "student", )

    def assessment_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:subjects_assessment_change", args=(obj.assessment.pk,)),
            obj.assessment
        ))
    assessment_link.short_description = "Assessment"

    def student_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:users_student_change", args=(obj.student.pk,)),
            obj.student
        ))
    student_link.short_description = "Student"

    ordering = ('-submitted_on', )

@admin.register(QAGrade)
class QAGradeAdmin(admin.ModelAdmin):
    list_display = ("id", "submission_link", "question_link", "mark", )
    list_filter = ("submission", "question", )

    def submission_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:subjects_assessmentsubmission_change", args=(obj.submission.pk,)),
            obj.submission
        ))
    submission_link.short_description = "Submission"

    def question_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:subjects_assessmentquestion_change", args=(obj.question.pk,)),
            obj.question
        ))
    question_link.short_description = "Question"

