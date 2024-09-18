FROM quay.io/devfile/universal-developer-image:latest

USER root

RUN useradd -rm -d /home/dagster -s /bin/bash -g root -u 1234 dagster
USER dagster

RUN python3 -m venv /tmp/venv
ENV PATH="/tmp/venv/bin:$PATH"
RUN pip3 install dagster dagster-webserver dagster_duckdb duckdb dbt-duckdb

USER root
RUN mkdir /superset
RUN chown dagster /superset

USER dagster
WORKDIR /superset
RUN pip3 install apache-superset duckdb-engine
RUN echo "SECRET_KEY='$(openssl rand -base64 42)'" > superset_config.py
RUN FLASK_APP=superset SUPERSET_CONFIG_PATH=superset_config.py superset db upgrade
RUN FLASK_APP=superset SUPERSET_CONFIG_PATH=superset_config.py superset fab create-admin --username admin --firstname admin --lastname admin --email admin@localhost --password admin
RUN FLASK_APP=superset SUPERSET_CONFIG_PATH=superset_config.py superset init
