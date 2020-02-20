from django.contrib import admin
from app.models import donor,bloodtype,yadmin,orderdata
# Register your models here.
admin.site.register(donor)
admin.site.register(bloodtype)
admin.site.register(yadmin)
admin.site.register(orderdata)
