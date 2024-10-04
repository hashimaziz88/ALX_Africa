# Movie Review API

Welcome to the **Movie Review API**! This Django-based API allows users to manage movie reviews, ratings, and recommendations. Users can create accounts, submit reviews, rate movies, and get personalized recommendations based on their preferences.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Running the API](#running-the-api)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- User authentication (registration and login)
- Create, read, update, and delete (CRUD) movie reviews
- Rate movies and see average ratings
- Get personalized movie recommendations
- Search and filter reviews by movie title
- Pagination for review lists
- User profiles for managing personal data

## Technologies

- **Django**: Web framework for building the API
- **Django REST Framework**: Toolkit for building Web APIs
- **PostgreSQL**: Database for storing user data and reviews
- **Django Allauth**: Authentication for user registration and login
- **Docker**: Containerization for easier deployment
- **Git**: Version control for the project code

## Getting Started

To get started with the Movie Review API, follow these steps to set up the project locally.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Movie_Review_API.git
   cd Movie_Review_API
   ```

````

2. **Create a virtual environment**:

   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:

   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Set up the database**:

   - Create a PostgreSQL database and user, and update the `DATABASES` setting in `settings.py` accordingly.
   - Run migrations:
     ```bash
     python manage.py migrate
     ```

6. **Create a superuser** (optional for admin access):
   ```bash
   python manage.py createsuperuser
   ```

### Running the API

1. **Start the server**:

   ```bash
   python manage.py runserver
   ```

2. **Access the API**:
   Open your browser and navigate to `http://127.0.0.1:8000/` to view the API endpoints.

### API Endpoints

| Endpoint                     | Method | Description                            |
| ---------------------------- | ------ | -------------------------------------- |
| `/`                          | GET    | Home page                              |
| `/search/`                   | GET    | Search for a movie                     |
| `/reviews/`                  | GET    | List all reviews                       |
| `/reviews/<int:pk>/`         | GET    | Retrieve a specific movie review       |
| `/reviews/new/`              | POST   | Create a new movie review              |
| `/reviews/<int:pk>/update/`  | PUT    | Update an existing movie review        |
| `/reviews/<int:pk>/delete/`  | DELETE | Delete a specific movie review         |
| `/reviews/<int:pk>/comment/` | POST   | Add a comment to a review              |
| `/reviews/<int:pk>/like/`    | POST   | Like a review                          |
| `/recommendations/`          | GET    | Get personalized movie recommendations |
| `/register/`                 | POST   | Register a new user                    |
| `/login/`                    | POST   | Login an existing user                 |
| `/logout/`                   | GET    | Logout the user                        |
| `/user-profile/`             | GET    | View user profile                      |
| `/user-profile/edit/`        | POST   | Edit user profile                      |

### Testing

To run tests for the application, execute the following command:

```bash
python manage.py test reviews
```

### Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request with your changes. Make sure to follow the code style guidelines and include tests for new features.

### License

This project is free to use and belongs to Hashim Aziz Muhammad, contact hashimazizm@gmail.com fr usage details.

### Acknowledgements

- [Django](https://www.djangoproject.com/) - The web framework used
- [Django REST Framework](https://www.django-rest-framework.org/) - For building the API
- [PostgreSQL](https://www.postgresql.org/) - Database system
- [Docker](https://www.docker.com/) - For containerization

````
