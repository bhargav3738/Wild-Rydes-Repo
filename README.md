# Flight Booking Service

A Django-based flight booking service application built with Docker, PostgreSQL, and MongoDB for efficient data management.

## Features

- Manage flight bookings efficiently.
- Utilizes PostgreSQL for relational data storage.
- MongoDB is integrated for NoSQL data handling.
- Dockerized setup for seamless deployment.

---

## Prerequisites

Ensure the following tools are installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Project Setup

### 1. Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/your-username/FlightBookingService.git
cd FlightBookingService
```
### 2 Set Up Environment Variables
Create a .env file in the root directory with the following environment variables:
```
#.env
# PostgreSQL
POSTGRES_DB=flight_db
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password

# MongoDB
MONGO_INITDB_ROOT_USERNAME=your_mongo_user
MONGO_INITDB_ROOT_PASSWORD=your_mongo_password

# Django

DJANGO_DEBUG=True
```

### 3. Build and Start the Application
```
#Build and start all the services using:

docker-compose up --build
```

### Managing the Application
#### Running Migrations
To apply database migrations:
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

Creating a Superuser
To create a Django admin superuser:
```
docker-compose exec web python manage.py createsuperuser
```
