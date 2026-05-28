from django.urls import path
from . import views

urlpatterns = [
    # Generic ListView
    path('', views.CourseListView.as_view(), name='index'),

    # Generic ListView
    path('instructors/', views.InstructorListView.as_view(), name='instructors'),

    # Generic DetailView — uses 'pk' by default to fetch the object
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),

    # Class Based View — handles GET and POST separately
    path('course/<int:course_id>/enroll/', views.EnrollView.as_view(), name='enroll'),

    # Function Based View — same result, different approach
    path('course/<int:course_id>/detail-fbv/', views.course_detail_fbv, name='course_detail_fbv'),
]