# Intro
This is an app to help The Good Registry to manage their orders

# How to start
1. Basic set up for local environment with Docker
```
$ docker-compose up
```
2. Install packages
```
$ pip freeze -r requirements.txt
```
3. Run the app in development mode
```
$ uvicorn app:app --reload // localhost: 8000
```
# Debug mode
```
$ python3 app.py // http://127.0.0.1:8001
```
# Reformat the code
```
$ black . 
```