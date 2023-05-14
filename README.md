# Casting Agency Capstone Project

## Capstone Project
This Capstone project is completed as part of the Udacity Full Stack Development nanodegree. The Casting Agency models a company that is responsible for creating movies and managing actors. This project currently only provides a back-end implementation of the casting agency with scope to include a front-end in a future update.

## Dependencies

1. Install required software:
  - Python 3.7
  - Virtual Environement
  - Postgres

2. Set up and populate the database:
With Postgres running, create a casting database:
`create database casting`

3. Create and activate a virtual environment:
```bash
py -m venv venv
venv/Scripts/activate
```

4. Install dependencies:
`pip3 install -r requirements.txt`

5. Run the application
```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

The application is run on `http://127.0.0.1:5000/` by default

## Hosting instructions
This project is hosted using Render. To host on Render, follow the below steps:
1. Create a Render account and log in
2. Set up a Postgres database by selecting New PostgresSQL
  - Provide a database new, select a tier and create the database
3. Create a new Web Service 
  - Link to the GitHub repo where the project is stored
  - Provide a name and select an instance type
  - Enter the build command: `pip install -r requirements.txt`
4. Connect the Web Service and Database
  - Open the database service and copy the internal database URL
  - Within the Web Service create an environment variable with the value of the previously copied URL
5. Save and wait for the build to complete. The service can now be accessed on the hosting URL.

## API Reference
### Getting Started
- Base URL: At present this app can be run locally and is hosted as a base URL: https://service-casting-capstone.onrender.com/.

### Authentication: 
There are currently three roles required to access all endpoints except for root. Authentication uses Bearer tokens. The three roles are:
- The Casting Assistant role can:
  -  view actors
  -  view movies
- The Casting Director role can:
  - all actions of a Casting Assistant plus:
  - update actors
  - update movies
  - add actors
  - delete actors
- The Executive Producer role can: 
  - all actions of a Casting Director plus:
  - add movies
  - delete movies

### Error Handling
Errors are returned as JSON objects in the following format:
```bash
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return five error types when requests fail:

- 400: Bad Request
- 401: Unauthorised
- 404: Resource Not Found
- 422: Not Processable
- 500: An unexpected error occured

### Endpoints

### Home

- General
  - Returns a success value to confirm home route is working correctly
- Sample `curl -r GET --url 'https://service-casting-capstone.onrender.com/'`
```bash
{
    "success": true
}
```

### Actors

#### GET /actors

- General
  - Returns a list of actors
- Sample `curl -r GET --url 'https://service-casting-capstone.onrender.com/actors' -H 'Authorization: Bearer {token}'`
```bash
{
  "actors": [
    {
      "age":58,
      "gender":"female",
      "id":1,
      "name":"Sandra Bullock"
    },
    {
      "age":66,
      "gender":"male",
      "id":9,
      "name":"Tom Hanks"
    }
  ],
  "success":true
}
```

#### POST /actors

- General
  - Creates a new actor with "name", "age" and "gender" fields required
- Sample `curl -r POST --url 'https://service-casting-capstone.onrender.com/actors' -H 'Authorization: Bearer {token}' -H 'Content-Type: application/json' -d '{"name": "Emma Watson", "age": 33, "gender": "female"}'`
```bash
{
    "age": 33,
    "gender": "female",
    "name": "Emma Watson",
    "success": true
}
```

#### PATCH /actors
- General 
  - Updates an actor by ID with "name", "age" and "gender" fields required
- Sample `curl -r PATCH --url 'https://service-casting-capstone.onrender.com/actors/11' -H 'Authorization: Bearer {token}' -H 'Content-Type: application/json' -d '{"name": "Emma Watson", "age": 35, "gender": "female"}'`
```bash
{
    "age": 35,
    "gender": "female",
    "name": "Emma Watson",
    "success": true
}
```

#### DELETE /actors
- General
  - Deletes an actor by ID
- Sample `curl -r DELETE --url 'https://service-casting-capstone.onrender.com/actors/12' -H 'Authorization: Bearer {token}' -H 'Content-Type: application/json'`
```bash
{
    "deleted": 11,
    "name": "Emma Watson",
    "success": true
}
```
### Movies

#### GET /movies

- General
  - Returns a list of movies
- Sample `curl -r GET --url 'https://service-casting-capstone.onrender.com/movies' -H 'Authorization: Bearer {token}'`
```bash
{
    "movies": [
        {
            "id": 2,
            "release_date": 2000,
            "title": "Castaway"
        }
    ],
    "success": true
}
```

#### POST /movies

- General
  - Creates a new movie with "title" and "release_date" fields required
- Sample `curl -r POST --url 'https://service-casting-capstone.onrender.com/movies' -H 'Authorization: Bearer {token}' -H 'Content-Type: application/json' -d '{"title": "Toy Story", "release_date": 1995}'`
```bash
{
    "release_date": 1995,
    "success": true,
    "title": "Toy Story"
}
```

#### PATCH /movies
- General 
  - Updates a movie by ID with "title" and "release_date" fields required
- Sample `curl -r PATCH --url 'https://service-casting-capstone.onrender.com/movies/6' -H 'Authorization: Bearer {token}' -H 'Content-Type: application/json' -d '{"title": "Toy Story", "release_date": 1997}'`
```bash
{
    "release_date": 1997,
    "success": true,
    "title": "Toy Story"
}
```

#### DELETE /movies
- General
  - Deletes a movie by ID
- Sample `curl -r DELETE --url 'https://service-casting-capstone.onrender.com/movies/7' -H 'Authorization: Bearer {token}' -H 'Content-Type: application/json'`
```bash
{
    "deleted": 7,
    "success": true,
    "title": "Toy Story"
}
```
