from django.contrib import admin
from .models import Category, PointSetting, BusinessHours

admin.site.register(Category)
admin.site.register(PointSetting)
admin.site.register(BusinessHours)