from django.contrib import admin
from .models import Group, Presentation

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'created_at']
    list_filter = ['teacher']

@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = ['title', 'group', 'uploaded_at']
    list_filter = ['group']