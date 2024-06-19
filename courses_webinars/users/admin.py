from django.contrib import admin
from users.models import UserWebinarLink, UserRootModuleLink, UserLessonLink, UserTaskLink

admin.site.register(UserWebinarLink)
admin.site.register(UserRootModuleLink)
admin.site.register(UserLessonLink)
admin.site.register(UserTaskLink)
