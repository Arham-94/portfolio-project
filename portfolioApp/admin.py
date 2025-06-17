from django.contrib import admin
from . import models
from .models import ContactMessage

# Register your models here.

admin.site.register(models.Profile)
admin.site.register(models.About)
admin.site.register(models.Skill)
admin.site.register(models.Education)
admin.site.register(models.Experience)
admin.site.register(models.Project)
admin.site.register(models.Profession)
admin.site.register(models.Service)
admin.site.register(models.SocialMedia)
admin.site.register(models.Color)
# admin.site.register(models.ContactMessage)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    