from django.contrib import admin
from users.models import UserWebinarLink, UserCourseLink, UserLessonLink

admin.site.register(UserWebinarLink)
admin.site.register(UserCourseLink)
admin.site.register(UserLessonLink)
