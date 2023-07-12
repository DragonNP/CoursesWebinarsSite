from django.contrib import admin
from .models import WatchedWebinar, WatchedCourse, WatchedLesson

admin.site.register(WatchedWebinar)
admin.site.register(WatchedCourse)
admin.site.register(WatchedLesson)
