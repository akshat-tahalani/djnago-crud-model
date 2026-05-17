from django.contrib import admin
from .models import User , Course ,Lesson ,Instructor



# Register your models here.

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Instructor)
# this acommand ios spexcifc to djangos admin panel to show 
#that data is managed using djangos auto genetrated data using uits ui

