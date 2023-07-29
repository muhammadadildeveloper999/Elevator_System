Elevator System Project

Overview
This is a Django-based Elevator System API that manages N elevators in a building. It provides endpoints for controlling elevator operations, handling user requests, and monitoring the system's status.

Features
Initialize the elevator system with N elevators.
Get the next destination floor for a specific elevator.
Make a user request to call an elevator to a floor.
Mark an elevator as not working or under maintenance.
Open and close the door of an elevator.
Requirements
Python 3.x
Django 3.x
Django REST Framework 3.x
Setup and Installation
Clone the repository: git clone https://github.com/muhammadadildeveloper999/Elevator_System.git
Create a virtual environment: python -m venv env
Activate the virtual environment.
Install the required packages: pip install -r requirements.txt
Set up the database 
Run migrations: python manage.py migrate
Create a superuser (optional): python manage.py createsuperuser
Start the development server: python manage.py runserver
API Endpoints
POST /api/initialize_elevator_system/
GET /api/{elevator_id}/next_destination/
POST api/make_request/
GET /api/{elevator_id}/mark_not_working/
GET /api/{elevator_id}/open_door/
GET /api/{elevator_id}/close_door/

Testing
Run test cases with: python manage.py test

License
This project is licensed under the MIT License.

For more details and usage examples, please refer to the complete README.md file in the repository.