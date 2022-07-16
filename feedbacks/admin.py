from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.safestring import mark_safe  


# Register your models here.
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("title", "created_on", "created_by", "subject")
    list_filter = ("created_on", "created_by", "subject")
    search_fields = ("title__startswith", )
    ordering = ("-created_on", )

@admin.register(FeedbackResponse)
class FeedbackResponseAdmin(admin.ModelAdmin):
    list_display = ("id", "feedback_link", "student_link", "submitted_on", )
    list_filter = ("submitted_on", "feedback", "student", )

    def student_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:users_user_change", args=(obj.student.user.pk,)),
            obj.student.user
        ))
    student_link.short_description = "Student"

    def feedback_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:feedbacks_feedback_change", args=(obj.feedback.pk,)),
            obj.feedback
        ))
    feedback_link.short_description = "Feedback"

    ordering = ("-submitted_on", )   
