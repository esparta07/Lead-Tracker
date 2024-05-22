from django.contrib import admin
from core.models import Lead, Source, Status,SubSource,Campaign
# Register your models here.

admin.site.register(Lead)
admin.site.register(Source)
admin.site.register(Status)
admin.site.register(SubSource)
admin.site.register(Campaign)
