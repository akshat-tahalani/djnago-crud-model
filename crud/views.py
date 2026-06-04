from urllib import request

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views import generic
from .models import Course, Enrollment, Instructor, Lesson, User, Courseprogress
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User as AuthUser
from django.shortcuts import redirect
#login is used to creat a session while logout is used to destroy it 

# authernticate is the vredential chekcer




# ════════════════════════════════════════════════════════════════
# GENERIC VIEWS — least code, most built-in behaviour
# Django automatically fetches all objects and passes to template
# ════════════════════════════════════════════════════════════════

def logout_request(request):
    logout(request)
    return redirect('index')

def login_request(request):
    context = {}
    if request.method == 'POST':
        # Pull username and password out of the POST data
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        if not username or not password:
            context['error'] = 'Username and password are required'
            return render(request, 'crud/login.html', context)
        
        # authenticate() returns user object if valid, None if invalid
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            # Wrong credentials — send back to login page with error
            context['error'] = 'Invalid username or password'
            return render(request, 'crud/login.html', context)
    return render(request, 'crud/login.html', context)

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'crud/register.html', context)
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        first_name = request.POST.get('firstname', '')
        last_name = request.POST.get('lastname', '')
        
        if not username or not password or not first_name or not last_name:
            context['error'] = 'All fields are required'
            return render(request, 'crud/register.html', context)
        
        user_exist = False
        try:
            AuthUser.objects.get(username=username)
            user_exist = True
        except:
            print("new user: " + username)
        if not user_exist:
            user = AuthUser.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            return redirect('index')
        else:
            context['error'] = 'Username already exists'
            return render(request, 'crud/register.html', context)

class CourseListView(generic.ListView):
    model = Course
    template_name = 'crud/index.html'
    context_object_name = 'courses'
    # you can also override the queryset to add filtering/ordering
    def get_queryset(self):
        # return all courses ordered by name
        return Course.objects.all().order_by('name')


class InstructorListView(generic.ListView):
    model = Instructor
    template_name = 'crud/instructors.html'
    context_object_name = 'instructors'


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'crud/course_detail.html'
    # DetailView automatically fetches a single object by pk or slug
    # passes it to template as 'object' or lowercase model name 'course'

    # override get_context_data to add extra data to template
    def get_context_data(self, **kwargs):
        # get the default context first
        context = super().get_context_data(**kwargs)
        # add lessons and instructors on top of it
        context['lessons'] = self.object.lesson_set.all()
        context['instructors'] = self.object.instructors.all()
        return context


# ════════════════════════════════════════════════════════════════
# CLASS BASED VIEW — manual get/post handling, full control
# ════════════════════════════════════════════════════════════════

class EnrollView(View):
    # get() handles GET requests to this URL
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        return render(request, 'crud/enroll.html', {'course': course})

    # post() handles POST requests (form submissions)
    def post(self, request, course_id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        course = get_object_or_404(Course, id=course_id)
        # enrollment logic goes here in future
        if request.user.is_authenticated:
            user = request.user
            # Check if the user is already enrolled in the course
            if not Enrollment.objects.filter(user=user, course=course).exists():
                Enrollment.objects.create(user=user, course=course)
        # after processing, redirect back to course detail
        # redirect to a new url called learning passing course id
        return HttpResponseRedirect(reverse('learning', args=(course_id,)))






# ════════════════════════════════════════════════════════════════
# FUNCTION BASED VIEW — plain Python function, explicit everything
# ════════════════════════════════════════════════════════════════

def course_detail_fbv(request, course_id):
    # manually fetch the course
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lesson_set.all()
    instructors = course.instructors.all()

    # manually handle GET vs POST inside one function
    if request.method == 'POST':
        # handle form submission
        return HttpResponseRedirect(reverse('course_detail', args=(course_id,)))

    # handle GET — just render the page
    context = {
        'course': course,
        'lessons': lessons,
        'instructors': instructors
    }
    return render(request, 'crud/course_detail.html', context)


class LearningView(View):
    def get(self, request, course_id):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        
        course = get_object_or_404(Course, id=course_id)
        lessons = course.lesson_set.all()
        
        # Get the user's enrollment
        enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
        
        # Get all course progress for this enrollment
        progress_list = Courseprogress.objects.filter(enrollment=enrollment)
        
        # Calculate statistics
        total_lessons = lessons.count()
        completed_count = progress_list.filter(completed=True).count()
        remaining_lessons = total_lessons - completed_count
        progress_percentage = int((completed_count / total_lessons * 100)) if total_lessons > 0 else 0
        
        # Build lessons data with completion status
        lessons_with_progress = []
        for lesson in lessons:
            progress = progress_list.filter(lesson=lesson).first()
            lessons_with_progress.append({
                'lesson': lesson,
                'completed': progress.completed if progress else False
            })
        
        context = {
            'course': course,
            'lessons': lessons_with_progress,
            'total_lessons': total_lessons,
            'completed_count': completed_count,
            'remaining_lessons': remaining_lessons,
            'progress_percentage': progress_percentage,
        }
        return render(request, 'crud/learning.html', context)