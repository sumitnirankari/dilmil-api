# DilMil REST API using Flask-Smorest and Docker
## postman collection 
[dilmil postman collection](https://raw.githubusercontent.com/sumitnirankari/dilmil-api/main/dilmil.postman_collection.json)
## To run the project:
    docker-compose up --build

It will run the web project on [localhost:5000](http://localhost:5000/swagger) and swagger on http://localhost:5000/swagger

## Other commands:
### To setup the project with fresh database:
#### clean `migrations` folder and `instance` folder
```
flask db init
```
```
flask db migrate -m 'initial migration'
```
```
flask db upgrade
```

### To build the docker:
```
docker build . -t dilmil-api
```

### To run the project on local:
```
source venv/bin/activate
```
```
pip install -r requirements.txt
```
```
pip install -r requirements-dev.txt
```
```
python app.py
```
To run testcases
```
pytest
```
