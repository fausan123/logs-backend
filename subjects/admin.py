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
