from django.contrib import admin
from .models import SharedFile, FileShareLink

class SharedFileAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'uploader', 'uploaded_at')
    list_filter = ('uploader', 'uploaded_at')
    search_fields = ('original_filename', 'uploader__username')

class FileShareLinkAdmin(admin.ModelAdmin):
    list_display = ('file', 'token', 'created_at', 'expires_at')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('file__original_filename', 'token')

admin.site.register(SharedFile, SharedFileAdmin)
admin.site.register(FileShareLink, FileShareLinkAdmin)