from django.contrib import admin
from .models import room, topic, message, User
# Register your models here.

admin.site.register(room)
admin.site.register(topic)
admin.site.register(message)
admin.site.register(User)

