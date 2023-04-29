**Agile Avengers**

## Project Overview

Easy Pay is a payment gateway application for businesses/individuals.<br/> 
Features of the application include:
- Sending payments
- Request payments

User level visualization include: 
- Expenditure in a Time duration
- Categorized spend
- Transaction history

For more information, please refer to [this](https://github.com/CSCI-5828-Foundations-Sftware-Engr/5828_s23/wiki/Payment-Gateway-Application:-Overview) detailed project overview.

## Setup
- [Pyenv](https://github.com/pyenv/pyenv) 
- Python: 
    - Required version - 3.7.6
- npm:
    - Required version - 6.14.4
- To run unit tests:
    - ```pip install pytest pytest-coverage```
- To run graybox tests:
    - ```pip install webdriver-manager```
    - ```pip install selenium```
    - ```pip install waitress```
    - ```pip install pytest-html```
- PostgreSQL: (Specific to Mac users)
    - Brew installation guide -> https://brew.sh/
    - ```brew install postgresql```
    - ```brew services start postgresql```
    - ```brew install node```

After cloning the repo,
- In the client directory,
    - ```cd agile-avengers/client/```
    - ```npm install```
- In the server directory, 
    - ```cd agile-avengers/server/```
    - ```python3 -m venv venv```
    - ```pip3 install -r requirements.txt```
    - ```source venv/bin/activate```
    - ```alembic upgrade head``` - upgrades all migration
    - ```alembic downgrade base``` - downgrades all migration - optional
    - ```alembic downgrade -<INTEGER>```- selective downgrade migration - optional

To start the application,   
-```cd agile-avengers/client/```
- ```npm run develop```
    - If for some reason because of error:0308010C:digital envelope routines::unsupported issues the server does not start, then run the command ```export NODE_OPTIONS=--openssl-legacy-provider```.
- ```cd agile-avengers/server/```
- ```source venv/bin/activate```
- ```flask run```

To start the server from kubernetes,

- This project needs ingress to expose backend service outside. To install ingress, run the following

    ```kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.7.0/deploy/static/provider/cloud/deploy.yaml```

- To learn more about ingress installation, you can refer [here](https://kubernetes.github.io/ingress-nginx/deploy)

-   To start the server, 
    - ```cd server```
    - ```make build``` to build the docker image. 
    - After building, run ```make deploy```. 
    - Then, the backend service will be available at `http://localhost/backend/`

To run the unit tests, 
- Ensure that the above mentioned packages are installed.
- `cd server`
- `make test` 

To run the graybox tests,
- Ensure that the above mentioned packages are installed.
- Ensure that the front end and back end servers are up and running.
- Ensure to install the browser and corresponding driver in order to execute the tests.
Chrome browser and ChromeDriverManager has been utilized here.
- Run the following commands:
    - ```cd /client/src/tests/graybox-tests``` 
    - ```pytest --html=report.html```. 
    - This will run all the files in the folder that have test_* as the file name and at the end, generate a HTML report which will state which test passed/failed.
- Note 1: There is a possibility that the URLs present in these test files might not work as these tests are dependent on the URL. Please keep an eye on it.
- Note 2: Each individual tests can be executed by running the command ```python <file-name>```. In order for the whole suite to be executed, the pytest command can be executed. **There is an dependency on the users utilized in these tests because of which the test can fail**
