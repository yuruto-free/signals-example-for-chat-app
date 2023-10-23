from django.contrib import admin
from . import models

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    model = models.Room
    fields = ['host', 'name', 'description', 'participants']
    list_display = ['host', 'name']
    ordering = ('-created_at',)

@admin.register(models.Config)
class ConfigAdmin(admin.ModelAdmin):
    model = models.Config
    fields = ['room', 'owner', 'order', 'offset']
    list_display = ['room', 'owner', 'order']
    ordering = ('-room', 'order')