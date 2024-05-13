# DilMil REST API using Flask-Smorest and Docker
postman collection 

To run the project:
    docker-compose up --build

Other commands:
To setup the project with fresh database:
    - clean `migrations` folder and `instance` folder
    - flask db init
    - flask db migrate -m 'initial migration'
    - flask db upgrade
To build the docker:
    docker build . -t dilmil-api

It will run the web project on [localhost:5000](http://localhost:5000/swagger) and swagger on http://localhost:5000/swagger

To run in local:
- source venv/bin/activate
- pip install -r requirements.txt
- pip install -r requirements-dev.txt
- python app.py
