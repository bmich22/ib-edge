from django.contrib import admin
from .models import Subject, UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'user_email',
        'user_first_name',
        'user_last_name',
        'is_tutor',
        'user_is_staff',
        'grade_year',
        'subject_list',  # ✅ Add subjects
    )
    list_filter = ('is_tutor', 'user__is_staff', 'subjects')
    search_fields = (
        'user__username',
        'user__email',
        'user__first_name',
        'user__last_name',
        'subjects__name',
    )
    filter_horizontal = ('subjects',)

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = 'First Name'

    def user_last_name(self, obj):
        return obj.user.last_name
    user_last_name.short_description = 'Last Name'

    def user_is_staff(self, obj):
        return obj.user.is_staff
    user_is_staff.boolean = True
    user_is_staff.short_description = 'Staff Status'

    def subject_list(self, obj):
        return ", ".join(subject.name for subject in obj.subjects.all())
    subject_list.short_description = 'Subjects'

