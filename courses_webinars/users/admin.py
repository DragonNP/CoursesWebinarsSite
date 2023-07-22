from django.contrib import admin
from users.models import UserWebinarLink, UserModuleLink, UserLessonLink

admin.site.register(UserWebinarLink)
admin.site.register(UserModuleLink)
admin.site.register(UserLessonLink)
