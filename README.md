# API User-Database Template
A simple API with a connection to a database of users that works out of the box.

It is also highly configurable just by changing the values in the `.env` file!

## Features
- Automatic database creation (if it does not exist)
  - The initial execution is interactive: It will prompt you in case you want to create the database
- Secure credentials through a `.env` file that contains all the important database information and credentials
```
    API_PRODUCTION=False
    API_PORT=8000
    
    DB_USER="postgres"
    DB_PORT=5432
    DB_HOST="localhost"
```
- Some level of error handling with the database connection
- The connection to the database closes automatically when the api is stopped
  - It uses the `atexit` library to close the connection
- It supports Virtual Environments with the use of `requirements.txt`
  - If the project is opened with PyCharm (recommended), it will automatically detect this and 
  create a virtual environment based on this requirements
- The users' passwords added to the database are automatically salted and encrypted (just the most basic level of security)

## Usage
Click on "[Use this template](https://github.com/simple-templates/api-userdb-template/generate)" and open the project. 
The recommended way to open it is by using PyCharm.

Then:
1. Design and code your own API --> [How to create a Flask API and document it with Swagger](https://www.imaginarycloud.com/blog/flask-python/)
2. Design and code your own SQL database and change the SQL code in the 
[Database.py](https://github.com/simple-templates/api-userdb-template/blob/91472ef31e52b6f6b0ebab88ec82666d0ad897b0/Database.py) file
3. Run the API and enjoy!

## Details
The API uses flask to get and send the requests, as well as to parse their header and body. 

The database is compatible with PostgreSQL. The SQL queries to create the database on start are hard-coded into the Database wrapper, this is something I am aware could be improved.

## LICENSE
[GPLv3](https://github.com/simple-templates/api-userdb-template/blob/df40f8cfa5c3cfbeee45554c7b9141031f45d1eb/LICENSE)
