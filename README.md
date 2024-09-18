# Try8 & Dagster Setup Guide

## Local Setup

### Build the docker container
```
$ docker build -t dagster-ecomm .
```
### Run & enter the container
```
$ docker run -it -p 3000:3000 -p 5000:5000 dagster-ecomm /bin/bash
```
### Get project
```
$ git clone https://github.com/try8ai/dagster-ecomm-demo-internal
$ cd dagster-ecomm-demo-internal
```
### Start dagster server
```
dagster dev -h 0.0.0.0
```
### Materialize assets
* In your browser, navigate to [localhost:3000](http://localhost:3000)
* Select *Assets*
* Select *View global asset lineage*
* Select *Materialize All*
### Start a new terminal in the container
```
$ docker container ls
$ docker exec -it <container_id> /bin/bash
```
### Run dbt
```
$ dbt run
```
### Run superset
```
$ cd /superset
$ FLASK_APP=superset SUPERSET_CONFIG_PATH=superset_config.py superset run -h 0.0.0.0
```
### Launch the superset UI
* In your browser, navigate to [localhost:5000](http://localhost:5000)
* Login Credentials: `admin:admin`
* Click the '+' icon in top right
* Select `Data` -> `Connect database`
* Type is "Other"
* SQLAlchemy URI: `duckdb:////home/dagster/dagster-ecomm-demo-internal/duckdb.duckdb`

From here you are able to create visualizations of the data
