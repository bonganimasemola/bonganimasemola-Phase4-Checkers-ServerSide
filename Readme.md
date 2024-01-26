Checkers Game Project

Introduction:
This project is written in react and python, flask for the api backend.

Features:
Interactive game board built with React & Flask
Getting Started
Bootstarting the project.

Front-End
Navigate to the server dir by using the cmd:

cd server
and run:

pipenv install && pipenv shell
starting the app you have to run the migration first and the will be though the trail of next cmd: run this cmd after installing flask in your enviroment

flask db init

flask db migrate -m 'message for the migration (treat this as the git of databases)'

flask db upgrade
then you can run the seed for the database:

python3 seed.py
to run the server you wil run the cmd:

python3 app.py
Front-End
then navigate to client and run the command:

cd client
then:

npm install
To start the front-end (client) you have to run the cmd:

npm start```

### Prerequisites
- Node.js and npm (You can download them [here](https://nodejs.org/))
- Python 3 and pip (Download from [python.org](https://www.python.org/))