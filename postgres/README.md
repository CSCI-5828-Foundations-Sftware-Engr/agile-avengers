# Postgres Service

### Getting started
To start the pod, run `make deploy`. This creates the persistent volume, persistent volume claim, deployment and service. To stop, run `make stop`. This deletes the associated kubectl deployment and service. To connect to the database in cli, run `make connect`

### Use
To use within another service, use the host as `postgres` and port `5432`