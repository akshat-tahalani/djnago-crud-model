from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Instructor, Course, Lesson

# View for homepage
def index(request):
    # Fetch all courses from the database
    courses = Course.objects.all()
    # Pass data to the template via context dictionary
    context = {'courses': courses}
    return render(request, 'crud/index.html', context)

# View for a single course detail
def course_detail(request, course_id):
    # get() fetches exactly one course by its id
    course = Course.objects.get(id=course_id)
    # Fetch all lessons belonging to this course — backward relationship
    lessons = course.lesson_set.all()
    # Fetch all instructors teaching this course — Many-To-Many forward
    instructors = course.instructors.all()
    context = {
        'course': course,
        'lessons': lessons,
        'instructors': instructors
    }
    return render(request, 'crud/course_detail.html', context)

# View for all instructors
def instructor_list(request):
    instructors = Instructor.objects.all()
    context = {'instructors': instructors}
    return render(request, 'crud/instructors.html', context)