from django.db import models
from django.contrib.auth.models import User as AuthUser

# User model — represents anyone using the platform
class User(models.Model):
    first_name = models.CharField(null=False, max_length=30, default='john')
    last_name  = models.CharField(null=False, max_length=30, default='doe')
    dob        = models.DateField(null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


# Instructor inherits from User — gets all User fields automatically
# Django creates a hidden One-To-One link between Instructor and User tables
class Instructor(User):
    full_time       = models.BooleanField(default=True)
    total_learners  = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} | Full-time: {self.full_time} | Learners: {self.total_learners}"


# Course — Many-To-Many with Instructor
# One course can have many instructors, one instructor can teach many courses
# Django auto-creates a hidden junction table to manage this relationship
class Course(models.Model):
    name        = models.CharField(null=False, max_length=100, default='online course')
    description = models.CharField(max_length=500)
    instructors = models.ManyToManyField(Instructor)

    def __str__(self):
        return f"{self.name} — {self.description}"


# Lesson — One-To-Many with Course (via ForeignKey)
# Each lesson belongs to exactly one course
# CASCADE means: if the course is deleted, all its lessons are deleted too
class Lesson(models.Model):
    title   = models.CharField(max_length=200, default="title")
    course  = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        course_name = self.course.name if self.course else "No Course"
        return f"{self.title} | Course: {course_name}"
    
class Enrollment(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course} on {self.date_enrolled}"
    

class Courseprogress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        status = "Completed" if self.completed else "In Progress"
        return f"{self.enrollment.user.username} - {self.lesson.title}: {status}"