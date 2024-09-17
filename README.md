Steps to run this project from within the unified container:

* `git clone https://github.com/try8ai/dagster-ecomm-demo-internal`
* `cd dagster-ecomm-demo-internal`
* `dagster dev`
* Go to Dagster web UI, materialize "Orders" asset
* `dbt run`
* `cd /superset; FLASK_APP=superset SUPERSET_CONFIG_PATH=superset_config.py superset run`
* Go to superset UI, click the '+' icon in top right, Data -> Connect database, type is "Other", SQLAlchemy URI: `duckdb:////home/dagster/dagster-ecomm-demo-internal/duckdb.duckdb`

Both `dagster` and `superset` support `-h` and `-p` flags to set the host and port to listen on. If running in Docker, set the host to `0.0.0.0` and the port to something exposed on the container (eg. `docker run -p 8081:8081`; then listening on port 8081).
