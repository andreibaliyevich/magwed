# magwed
 Magazine wedding


## Project Overview

MAGWED is a web portal designed to help couples find wedding organizers in a selected city. The platform provides functionality similar to a social network, allowing users to browse organizer profiles, view photo albums and individual photos, leave likes, reviews, and comments, and communicate via an internal chat system.


## Installation

The project is deployed using Docker.

### Prerequisites

- Docker
- Docker Compose

### Setup Instructions

##### 1. Clone the repository

    git clone https://github.com/andreibaliyevich/magwed.git

##### 2. Navigate to the project directory

    cd magwed

##### 3. Create a .env file with environment variables in the backend directory

Example:

    SECRET_KEY=secret_key
    SQL_NAME=sql_name
    SQL_USER=sql_user
    SQL_PASSWORD=sql_password
    EMAIL_HOST_USER=email_host_user
    EMAIL_HOST_PASSWORD=email_host_password
    EMAIL_HOST_RECEIVER=email_host_receiver

##### 4. Create a .env file with environment variables in the frontend directory

    NODE_OPTIONS=--no-warnings

##### 5. Create a .env file with environment variables in the postgres directory

Example:

    POSTGRES_DB=sql_name
    POSTGRES_USER=sql_user
    POSTGRES_PASSWORD=sql_password

##### 6. Build Docker images

    docker compose build

##### 7. Start a bash session in the backend service

    docker compose run backend bash

##### 8. Apply database migrations

    python manage.py migrate

##### 9. Compile localization files

    django-admin compilemessages

##### 10. Create a superuser account

    python manage.py createsuperuser

##### 11. Exit the bash session

    exit

##### 12. Start all services

    docker compose up


## License

This project is licensed under the
[The MIT License](https://opensource.org/license/mit)
