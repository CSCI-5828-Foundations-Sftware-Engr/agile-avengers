**Agile Avengers**

Setup pyenv - https://github.com/pyenv/pyenv
Python version - 3.7.6
npm version - 6.14.4

Installing - Mac only guide - Sorry windows friends

1. Brew installation guide -> https://brew.sh/
2. brew install postgresql
3. brew services start postgresql
4. brew install node

cd client; npm install

Steps to follow for requirement installations:

1. cd agile-avengers/client/
2. npm install
3. cd agile-avengers/server/
4. Make sure you have python3 pointing to version 3.7.6
5. python3 -m venv venv
6. pip3 install -r requirements.txt
7. source venv/bin/activate
8. alembic upgrade head - upgrades all migration
9. alembic downgrade base - downgrades all migration - optional
10. alembic downgrade -<INTEGER> - selective downgrade migration - optional




Start application

1. cd agile-avengers/client/; npm run develop
2. cd agile-avengers/server/; source venv/bin/activate; flask run
