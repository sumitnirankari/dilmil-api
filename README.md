# DilMil REST API using Flask-Smorest and Docker
postman collection 
 - https://api.postman.com/collections/2877245-a7a538ab-b300-458f-bf14-885980302550?access_key=PMAT-01HXRQGXN5PFPN2DFY74KW33Q2

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
