# Image link - https://hub.docker.com/r/centos/python-38-centos7
FROM registry.access.redhat.com/ubi8/python-38

USER root
# Changing user of default user which is set to 1001
RUN usermod -u 1002 default
RUN groupadd -g 1001 svc_jenkins
RUN useradd -g svc_jenkins -d /home/svc_jenkins -m -s /bin/bash svc_jenkins -u 1001

# Installing python code requirements
COPY ./server/requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update -y --nobest && \
    apt-get install -yqq nodejs vim-enhanced && \
    npm i -g npm@^6 && \
    npm i -g webpack webpack-cli
RUN mkdir /app && chown -R svc_jenkins:svc_jenkins /app && chown -R svc_jenkins:svc_jenkins /home/svc_jenkins
RUN chown -R svc_jenkins:svc_jenkins /opt/app-root/src/.npm
RUN chown -R svc_jenkins:svc_jenkins /app

USER svc_jenkins

# Copying folders into the container
ADD --chown=svc_jenkins:svc_jenkins ./server /app/server
ADD --chown=svc_jenkins:svc_jenkins ./client /app/client

WORKDIR /app

# Exposing 5000 tcp port 
EXPOSE 5000

COPY --chown=svc_jenkins:svc_jenkins client/package.json ./

# installing front end dependecies
RUN npm install --no-optional --development  && npm cache clean --force && cd client && npm run webpack

# Starting gunicorn to bring up frontend
CMD cd /app/server/ &&  gunicorn -b :5000 --worker-tmp-dir /dev/shm --workers=5 --timeout 120 flask_app:app --worker-class gevent --log-level=debug --log-file=/app/server/gunicorn.log