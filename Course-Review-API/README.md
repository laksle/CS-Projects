Course Review API

A Dockerized course review backend built with Python, Flask, SQLite, and REST APIs. 
The application uses separate microservices for users, courses, and reviews, with JWT-based authentication.

This projects features the following functionality :

- User registration and login
- Custom JWT authentication
- Password hashing
- Course creation and retrieval
- Course reviews with ratings and difficulty scores
- Dockerized microservices
- Separate SQLite database for each service
- Inter-service communication over a Docker network


The application is divided into three services:

Users Service
- Handles registration and login
- Stores user accounts
- Creates and verifies JWTs

Courses Service
- Creates and retrieves courses
- Stores course information

 Reviews Service
- Creates and retrieves course reviews
- Validates authentication through the Users service
- Validates courses through the Courses service
- Calculates course rating and difficulty averages

Running in Docker:
TO run this in docker, open terminal in the location of the docker-compose file. 
Then run the following commands: 
docker compose build
docker compose up

You can test the API functionality by commands through the terminal
For example, the following curl command creates a user in a windows cmd terminal
curl -X POST http://localhost:9000/register -H "Content-Type: application/json" -d "{\"username\":\"testuser\",\"password\":\"password123\"}"

To login, a example command would be:
curl -X POST http://localhost:9000/login -H "Content-Type: application/json" -d "{\"username\":\"testuser\",\"password\":\"password123\"}"

To verify token, a example command would be:
curl http://localhost:9000/verify -H "Authorization: Bearer YOUR_TOKEN"

To create a course, a example command would be:
curl -X POST http://localhost:9001/courses -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" -d "{\"code\":\"CSE123\",\"name\":\"Software Design\",\"professor\":\"Test Professor\"}"
