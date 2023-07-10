from django.contrib import admin

from user_profile.models import Profile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_details', 'profile_pic', 'gender')


admin.site.register(Profile, UserProfileAdmin)
