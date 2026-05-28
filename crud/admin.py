from django.contrib import admin
from .models import User, Instructor, Course, Lesson

# ── INLINE CLASSES ────────────────────────────────────────────────

# LessonInline — shows lessons inside the Course admin page
# StackedInline shows each related object as a full form block
class LessonInline(admin.StackedInline):
    model = Lesson      # which model to show inline
    extra = 2           # how many empty extra forms to show by default


# TabularInline shows related objects as a compact table row instead
# Swap StackedInline for TabularInline to see the difference
class LessonTabularInline(admin.TabularInline):
    model = Lesson
    extra = 1


# Admin class for User — customizes how User appears in admin
class UserAdmin(admin.ModelAdmin):
    # list_display controls which columns show in the list view
    list_display = ['first_name', 'last_name', 'dob']
    
    # list_filter adds a filter sidebar on the right
    list_filter = ['first_name']
    
    # search_fields adds a search bar at the top
    search_fields = ['first_name', 'last_name']


# Admin class for Instructor
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'full_time', 'total_learners']
    
    # filter by full_time status — shows True/False sidebar filter
    list_filter = ['full_time']
    
    search_fields = ['first_name', 'last_name']


# Admin class for Course
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


# Admin class for Lesson
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']
    
    # filter lessons by which course they belong to
    list_filter = ['course']
    
    search_fields = ['title']


# Register each model WITH its admin class
# Now Django knows to use your custom admin class instead of the default
admin.site.register(User, UserAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)