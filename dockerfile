FROM python:3.8.10

USER root

COPY server/requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt 

RUN apt-get update -y && \
    apt-get install -yqq nodejs npm && \
    npm i -g npm@^6 && \
    npm i -g webpack webpack-cli

COPY client /app/client

RUN cd /app/client && npm install --no-optional --development  && npm cache clean --force && cd /app/client && npm run webpack

# For some reason, keycloak installed from requirements.txt does not work.
# Do not move the below two dependencies to requirements.txt

RUN pip install keycloak-client==0.15.4

RUN pip install python-keycloak==2.15.3

COPY server/flask_app.py server/alembic.ini server/start.sh server/db_queries.py /app/

COPY server/alembic /app/alembic

COPY server/config /app/config

COPY server/datamodel /app/datamodel

COPY server/helpers /app/helpers

WORKDIR /app
# Starting gunicorn to bring up frontend
# CMD cd /app/server/ &&  gunicorn -b :5000 --worker-tmp-dir /dev/shm --workers=5 --timeout 120 flask_app:app --worker-class gevent --log-level=debug --log-file=/app/server/gunicorn.log

ENTRYPOINT [ "bash",  "start.sh" ]