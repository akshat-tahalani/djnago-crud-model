import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courseapp.settings')
django.setup()

from crud.models import Course, Instructor, Lesson

# Create sample instructors
instructor1 = Instructor.objects.create(
    first_name="John",
    last_name="Smith",
    full_time=True,
    total_learners=150
)

instructor2 = Instructor.objects.create(
    first_name="Jane",
    last_name="Doe",
    full_time=True,
    total_learners=200
)

# Create sample courses
course1 = Course.objects.create(
    name="Python Basics",
    description="Learn the fundamentals of Python programming"
)
course1.instructors.add(instructor1)

course2 = Course.objects.create(
    name="Web Development with Django",
    description="Master Django framework for building web applications"
)
course2.instructors.add(instructor1, instructor2)

# Create sample lessons
Lesson.objects.create(
    title="Introduction to Python",
    course=course1,
    content="Python is a high-level programming language known for its simplicity and readability."
)

Lesson.objects.create(
    title="Variables and Data Types",
    course=course1,
    content="Learn about variables, integers, strings, lists, and dictionaries in Python."
)

Lesson.objects.create(
    title="Getting Started with Django",
    course=course2,
    content="Django is a web framework that makes web development faster and easier."
)

Lesson.objects.create(
    title="Models and Database",
    course=course2,
    content="Create database models and manage data using Django ORM."
)

print("✓ Sample data created successfully!")
print(f"Courses: {Course.objects.count()}")
print(f"Instructors: {Instructor.objects.count()}")
print(f"Lessons: {Lesson.objects.count()}")
