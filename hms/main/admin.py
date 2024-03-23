from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(HallManager)
admin.site.register(Complaint)
admin.site.register(Notice)
admin.site.register(Hall)
admin.site.register(Payments)
admin.site.register(StudentPayment)
admin.site.register(StudentPassbook)
admin.site.register(Due)
