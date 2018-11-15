![license](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Build Status](https://travis-ci.com/BrianSerem/Send-It-API.svg?branch=develop)](https://travis-ci.com/BrianSerem/Send-It-API)
[![Coverage Status](https://coveralls.io/repos/github/BrianSerem/Send-It-API/badge.svg?branch=develop)](https://coveralls.io/github/BrianSerem/Send-It-API?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/609b635d8231deaa3689/maintainability)](https://codeclimate.com/github/BrianSerem/Send-It-API/maintainability)

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

### Create and activate a virtual environment

    virtualenv env --python=python3.6

    source env/bin/activate

### Install required Dependencies

    pip install -r requirements.txt

## Running the application

```
$ export FLASK_APP="run.py"
$ export FLASK_DEBUG=1
$ export APP_SETTINGS="development"
```
### Open Terminal and type
$ flask run

### Open postman and use the below endpoints.


## Endpoints currently available
| Method | Endpoint                        | Description                           | User-type         |
| ------ | ------------------------------- | ------------------------------------- | ------------  |
|1.POST   | /api/v1/parcels                | Creates a new parcel order.           | customers        |
|2.GET   | /api/v1/parcels                 | get all parcel orders                    | admin         |
|3.GET    |/api/v1/parcels/int      | Get a specific parcel order          | customers/admin   |
| 4.GET    | /api/v1/parcels/approved          | get approved parcel orders            | Admin/customer         |
| 5.GET    | /api/v1/parcels/approved         | gets all approved parcel orders       |Admin/customer           |
|6. GET    |/api/v1/parcels/declined         | gets all declined orders              | Admin         |
| 7.GET    | /api/v1/parcels/moving          | gets all parcel orders currently in transit | Custormer/Admin        |
|8. GET   | /api/v1/parcels/approved              | gets all pending parcel orders              | Users/Admin   |
|9. PUT    | /api/v1/parcels/int/delivered   | changes parcel status to delivered           | Admin    |
|10. PUT    | api/v1/parcels/int/approved          | changes parcel status to approved                | Admin   |
|11. PUT | /api/v1/parcels/int/declined               | changes parcel status to declined              | Admin   |
| 12.PUT    | /api/v1/parcels/int/moving     | changes parcel status to moving                    | Admin         |
| 13.PUT    | /api/v1/parcels/int/cancel     | cancels a parcel order     | custormer         |
| 14.PUT    | /api/v1/users/int/parcels      | gets all parcels orders for a user               | Admin         |
| 15.POST    | /api/v1/parcels/int/destination| changes parcel order destination             | custormer    



	`
## How to test the hosted version:
Heroku app hosted on: sendit123.herokuapp.com/
place the different endpoints at the end of the above url to test
>>>>>>> 365bb87e8f510d597f66d40541babb145bfcbdb7
