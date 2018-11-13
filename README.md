![license](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Build Status](https://travis-ci.com/BrianSerem/Send-It-API.svg?branch=ft-final-file-structre-161859299)](https://travis-ci.com/BrianSerem/Send-It-API)
[![Coverage Status](https://coveralls.io/repos/github/BrianSerem/Send-It-API/badge.svg?branch=ft-final-file-structre-161859299)](https://coveralls.io/github/BrianSerem/Send-It-API?branch=ft-final-file-structre-161859299)


# Send-It-API
api for sendit application, an pp used for sending and tracking parcels across the country

This project shows one of the possible ways to implement RESTful API server.

There are two implemented models: User and Todo, one user has many todos.

## _Main libraries used_:

1. Flask-RESTful - restful API library.
2. Flask-Script - provides support for writing external scripts.



## Running 

1. Clone repository.

https://github.com/BrianSerem/Send-It-API.git

2. Create and activate a virtual environment inside the folder after cloning

source  <environmentname>/bin/activate

2. Install the dependencieslone 
	`pip install requirements.txt`
 
3. Cd into app where run.py is located.
cd app
  

4. How to run the app.
STEP 1: export to flask through: export FLASK_APP=run.py 
STEP 2: do flask run to start the server and run the app
	`
## How to test the hosted version:
Heroku app hosted on: sendit123.herokuapp.com/
place the different endpoints at the end of the above url to test
