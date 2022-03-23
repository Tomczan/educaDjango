import requests

username = ''
password = ''

base_url = 'http://127.0.0.1:8000/api/'

# pobranie wszystkich kursów
r = requests.get(f'{base_url}courses/')
courses = r.json()

available_courses = ', '.join([course['title'] for course in courses])
print(f'Dostepne kursy: {available_courses}')

for course in courses:
    course_id = course['id']
    course_title = course['title']
    r = requests.post(f'{base_url}courses/{course_id}/enroll/',
                      auth=(username, password))

    if r.status_code == 200:
        # zadanie zakonczone pomyslnie
        print(f'Pomyslnie zapisales sie na kurs {course_title}')
