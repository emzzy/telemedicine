# Telemedicine

## Whats this?
This is a full stack telemedicine application designed to deliver messaging through a secure text based communication between two clients, consultations, and essential medical services.

## Why this?
I was inspired by the lack of emergency medical assistance in rural and developing regions. A condition that puts the residents at a disadvantage leaving them without access to basic medical healthcare, most especially during emergency situations.

## Built with
Python, Django, Django Rest Framework, Swagger, Redis, Channels, Docker

# Key Features
 Secure Chat messaging: Real time text chats for symptom updates, follow ups, or general communication.
 JWT Authentication: Secure login and session management using JSON Web Tokens.
 Appointment Scheduling: Patient can book, reschedule, or cancel appointment with healthcare professionals.
 Scalable Architecture: Built with Django, Channels, Redis, Django Rest Framework, Docker for performance reliability.
 Medical Records Access: Users can view and manage helath history.
 Emergency ready design: Optimized for low bandwith environments and quick access to healthcare.

## Getting Started
Prerequisites
run pip install requirements.txt
## Installation
1. Clone the repo 
    git clone [https://](https://github.com/emzzy/telemedicine.git)
    cd telemedicine
2. Create and activate a virtual environemnt
    python -m venv venv
    source venv/bin/activate
3. Install dependencies
    pip install requirements.txt
4. Apply migrations
    python manage.py makemigrations
    python manage.py migrate