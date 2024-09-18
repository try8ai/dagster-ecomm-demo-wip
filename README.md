# Try8 & Dagster Setup Guide

## Local Setup

### Build & run the demo container

In your terminal run
```
$ docker build -t dagster-ecomm .
$ docker run -it -p 3000:3000 -p 5000:5000 dagster-ecomm /bin/bash
```

### Get project & start dagster server

In the demo container run
```
$ git clone https://github.com/try8ai/dagster-ecomm-demo-internal
$ cd dagster-ecomm-demo-internal
$ dagster dev -h 0.0.0.0 > /dev/null 2>&1 &
```

### Materialize assets

* In your browser, navigate to [localhost:3000](http://localhost:3000)
* Select *Assets*
* Select *View global asset lineage*
* Select *Materialize All*

### Run dbt & superset
```
$ dbt run
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
