# Telemedicine

## Whats this?
This is a full stack telemedicine application designed to deliver messaging through a secure text based communication between two clients, consultations, and essential medical services.

## Why this?
I was inspired by the lack of emergency medical assistance in rural and developing regions. A condition that puts the residents at a disadvantage leaving them without access to basic medical healthcare, most especially during emergency situations.

## Built with
* Python 
* Django 
* Django Rest Framework 
* Swagger 
* Redis 
* Channels
* Docker

## Key Features
- [x] Secure Chat messaging: Real time text chats for symptom updates, follow ups, or general communication.
- [x] JWT Authentication: Secure login and session management using JSON Web Tokens.
- [x] Appointment Scheduling: Patient can book, reschedule, or cancel appointment with healthcare professionals.
- [x] Scalable Architecture: Built with Django, Channels, Redis, Django Rest Framework, and Docker for performance reliability.
- [x] Medical Records Access: Users can view and manage helath history.
- [x] Emergency ready design: Optimized for low bandwith environments and quick access to healthcare.
- [x] Swagger API Documentation: Interactive API exploration and testing.
- [x] Email Notifications: Notity users with email integraton.

## Getting Started
Run
 ```py 
 pip install requirements.txt 
 ```
### Installation
1. Clone the repo
    ```
    git clone https://github.com/emzzy/telemedicine.git
    cd telemedicine
    ```
2. Create and activate a virtual environemnt
    ```
    python -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies
    pip install requirements.txt
    
4. Apply migrations
    ```
    cd backend/src
    python manage.py makemigrations
    python manage.py migrate
    ```
