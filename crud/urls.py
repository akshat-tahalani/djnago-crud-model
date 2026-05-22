from django.urls import path
from . import views

# Each path() maps a URL pattern to a view function
urlpatterns = [
    path('', views.index, name='index'),                              # /
    path('instructors/', views.instructor_list, name='instructors'),  # /instructors/
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),  # /course/1/
]