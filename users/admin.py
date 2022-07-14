from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe  
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_approved', 'is_student')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Contact info', {'fields': ('email', )}),)
  
    list_display = ("first_name", "last_name", "email", "date_joined", "is_student", "is_approved")
    list_filter = ("date_joined", "is_approved", "is_student",)
    search_fields = ("first_name__startswith", )
    ordering = ("-date_joined", )

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("id", "user_link", "dob", "phonenumber", "position", "is_approved")
    list_filter = ("position", )

    def user_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:users_user_change", args=(obj.user.pk,)),
            obj.user
        ))
    user_link.short_description = "Faculty"    

    def is_approved(self, obj):
        return obj.user.is_approved
    is_approved.boolean = True

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("admission_number", "user_link", "dob", "guardian_name", "class_name", )
    list_filter = ("class_name", )

    def user_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:users_user_change", args=(obj.user.pk,)),
            obj.user
        ))
    user_link.short_description = "Student"    
