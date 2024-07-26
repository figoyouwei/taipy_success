# taipy_deploy_heroku
This is a sample code that tests the deployment on heroku

## Local versions
- 2024.07.25: Check-in
- 2024.07.26: Change project name to tapiy_success

## main.py
- Create instances of data models (pydantic).
- Create instances of page models (taipy).
- Run GUI

## Docker steps
- Create .dockerignore
- Create Dockerfile
- Create Dockerimage with export-docker.py
- Run Dockerapp with
```
docker run -p 9000:9000 IMAGE-ID
```
