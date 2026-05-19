from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, InternshipPlacement, WeeklyLog, EvaluationCriteria, Evaluation

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'university_id', 'is_staff', 'is_superuser']
    list_filter = ['role', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'university_id']
    fieldsets = UserAdmin.fieldsets + (
        ("Role Information", {"fields": ("role", "university_id")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (

        ("Role Information", {"fields": ("role", "university_id")}),
    )
admin.site.register(CustomUser, CustomUserAdmin)

class InternshipPlacementAdmin(admin.ModelAdmin):
    list_display = ['student', 'company_name', 'course', 'Academic_supervisor', 'work_supervisor', 'is_active']
    search_fields = ['student__username', 'company_name', 'Academic_supervisor__username', 'work_supervisor__username']
    list_filter = ['is_active','course']
admin.site.register(InternshipPlacement, InternshipPlacementAdmin)

class WeeklyLogAdmin(admin.ModelAdmin):
    list_display = ['placement', 'week_number', 'status', 'created_at']
    list_filter = ['status', 'week_number']
    search_fields = ['placement__student__username', 'activities']
admin.site.register(WeeklyLog, WeeklyLogAdmin)

class EvaluationCriteriaAdmin(admin.ModelAdmin):
    list_display = ['name', 'weight']
    search_fields = ['name']
admin.site.register(EvaluationCriteria, EvaluationCriteriaAdmin)

class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['criteria', 'log', 'supervisor', 'score']
    search_fields = ['criteria__name', 'log__placement__student__username', 'supervisor__username']
admin.site.register(Evaluation, EvaluationAdmin)


