import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courseapp.settings')
django.setup()

from crud.models import Course
from django.test import RequestFactory
from crud.views import course_detail
from django.template.loader import render_to_string

# Check database
courses = Course.objects.all()
print(f"Courses in DB: {courses.count()}")
for c in courses:
    print(f"  {c.id}: {c.name}")

# Test the view
factory = RequestFactory()
request = factory.get('/course/1/')
response = course_detail(request, 1)

print(f"\nView Response Status: {response.status_code}")
print(f"View Response Content Length: {len(response.content)}")

# Check if form is in response
content = response.content.decode()
print(f"Has '<form': {'<form' in content}")
print(f"Has 'Enroll': {'Enroll' in content}")
print(f"Has '.btn-green': {'.btn-green' in content}")

# Print first 2000 chars
print("\n--- RESPONSE CONTENT ---")
print(content[content.find('<body>'):content.find('</body>')+7])
