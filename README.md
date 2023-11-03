# academic_teach

`academic_teach` is an educational website that allows students to purchase and enroll in predefined courses.

## Description

This project provides a platform where students can browse and select a list of available courses. After registering on the site and choosing the courses they want, they can buy and register on it. Students will have access to their user panel, where they can view their course details and schedule, can also edit their user profile.
Also teachers have access to their user panel and can see their courses and in the details, in addition to the course details, they can also see their students.

## Models

The project utilizes the following models:

- **User**: Customized Django User model
- **Student**: Inherited from the User model and stores the details of students.
- **Teacher**: Inherited from the User model and stores the details of teachers.
- **Lesson**: Contains details about the courses available on the website, such as lesson title, description, and associated teacher.
- **Enrollment**: Tracks students enrollment in specific courses, including student, course, and enrollment date.

## Features

- Create, read, update, and delete (CRUD) operations for books
- User authentication system
- Efficient image management using the `Pillow` package
- User-friendly messages and notifications with the `Sweetify` package
- Conversion of dates from the Gregorian calendar to the solar calendar using the `Django-Jalali-Date` package
- Image optimization and performance enhancement with the `Sorl-Thumbnail` package
- Render partials using `django-render-partial` package

## Installation and Setup

1. Clone the project from the GitHub repository:

```
git clone https://github.com/MuGhasemi/academic_teach.git
```

2. Navigate to the project directory and activate the virtual environment:

```
cd academic_teach
python -m venv venv
source venv/bin/activate
```

3. Install project dependencies:

```
pip install -r requirements.txt
```

4. Run the migrations:

```
python manage.py migrate
```

5. Start the development server:

```
python manage.py runserver
```

The project will now be accessible on your local development environment. Open your web browser and visit the provided URL to access the website.

## Contributing

If you are interested in contributing to the project, feel free to share feedback, ideas, and bug reports through the Issues section and submit Pull Requests on GitHub.


## Contributors:

If you have any questions or requests, you can contact me:

- Backend Developer: [Muhammad Ghasemi](https://github.com/MuGhasemi)
- Frontend Developer: [Reza Mohammadzade](https://github.com/reza-sdo)