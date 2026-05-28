import requests
import time

time.sleep(3)  # Wait for container to be ready

try:
    r = requests.get('http://localhost:8000/course/1/')
    print(f'Status: {r.status_code}')
    print(f'Has Enroll: {"Enroll" in r.text}')
    print(f'Has form: {"<form" in r.text}')
    if '<form' in r.text:
        idx = r.text.find('<form')
        print(f'\n✅ SUCCESS! The Enroll Now button is now visible in Docker container')
        print(r.text[idx:idx+300])
    else:
        print('❌ Form still not found')
except Exception as e:
    print(f'Error: {e}')
