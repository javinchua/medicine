from django.contrib import admin
from .models import User, Time, Medicine
# Register your models here.
admin.site.register(User)
admin.site.register(Time)
admin.site.register(Medicine)