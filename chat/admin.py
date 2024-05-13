from django.contrib import admin

from .models import Thread, Message

admin.site.register((Thread, Message))

admin.site.site_header = "Admin panel"