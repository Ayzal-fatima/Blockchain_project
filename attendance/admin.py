from django.contrib import admin
import os
from django.conf import settings


from attendance_system.settings import BASE_DIR
from blockchain.facial_recognition_service import register_face

from .models import UserProfile, BiometricData, AttendanceRecord
 

class BiometricDataAdmin(admin.ModelAdmin):
    list_display = ['username', 'user_profile_image', 'facial_encoding']
    search_fields = ['user__username']
    list_select_related = ['user']

    def username(self, obj):
        return obj.user.username
    username.short_description = 'User'

    def user_profile_image(self, obj):
        return obj.user.userprofile.image.url if obj.user.userprofile.image else 'No Image'
    user_profile_image.short_description = 'User Profile Image'





class UserProfileAdmin(admin.ModelAdmin):
    actions = ['create_user_profile']

    def create_user_profile(self, request, queryset):
        for user_profile in queryset:
            user_id = user_profile.user.id
            image = user_profile.image

            if image:
                # Use settings.MEDIA_ROOT to construct the image path
                image_path = os.path.join(settings.MEDIA_ROOT, user_profile.image.name)

                # Create or update the user's biometric data
                user_biometric, created = BiometricData.objects.get_or_create(user=user_profile.user)
                encoding = register_face(image_path)

                if encoding:
                    user_biometric.set_encoding(encoding)
                    user_biometric.save()
                    user_profile.user.profile_created = True
                    user_profile.user.save()

                    self.message_user(request, f"Face registered successfully for user {user_profile.user.username}.")
                else:
                    self.message_user(request, f"No face detected in the image for user {user_profile.user.username}.")
            else:
                print(f"Processing user ID: {user_id}, No image available for encoding")
    
    create_user_profile.short_description = "Create or update user profiles with biometric data"










class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'timestamp', 'authentication_method', 'status']
    list_filter = ['date', 'status']
    list_editable = ['status']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(BiometricData, BiometricDataAdmin)
admin.site.register(AttendanceRecord, AttendanceRecordAdmin)






























# class UserProfileAdmin(admin.ModelAdmin):
#     actions = ['create_user_profile']

#     def create_user_profile(self, request, queryset):
#         for user_profile in queryset:
#             user_id = user_profile.user.id
#             image = user_profile.image

#             if image:
#                 # Use settings.MEDIA_ROOT to construct the image path
#                 image_path = os.path.join(settings.MEDIA_ROOT, user_profile.image.name)

#                 # Create or update the user's biometric data
#                 user_biometric, created = BiometricData.objects.get_or_create(user=user_profile.user)
#                 encoding = register_face(image_path)

#                 if encoding:
#                     user_biometric.set_encoding(encoding)
#                     user_biometric.save()
#                     user_profile.user.profile_created = True
#                     user_profile.user.save()
#             else:
#                 print(f"Processing user ID: {user_id}, No image available for encoding")

